import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

import mlflow
import xgboost as xgb
from hyperopt import STATUS_OK, Trials, hp, tpe, fmin
from hyperopt.pyll import scope
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

TRACKING_SERVER_HOST = os.getenv("AWS_EC2_PEUBLIC_DNS")
MLFLOW_TRACKING_URI = f"http://{TRACKING_SERVER_HOST}:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)


from prefect import flow, task
from prefect.deployments import DeploymentSpec
from prefect.flow_runners import SubprocessFlowRunner
from prefect.task_runners import SequentialTaskRunner
from prefect.orion.schemas.schedules import IntervalSchedule

search_space = {
    "max_depth": scope.int(hp.quniform("max_depth", 4, 100, 1)),
    "learning_rate": hp.loguniform("learning_rate", -3, 0),
    "reg_alpha": hp.loguniform("reg_alpha", -5, -1),
    "reg_lambda": hp.loguniform("reg_lambda", -6, -1),
    "min_child_weight": hp.loguniform("min_child_weight", -1, 3),
    "objective": "reg:linear",
    "seed": 42,
}

model_name = "house-price-regressor"


@task
def read_prepare_data(path):
    train = pd.read_csv(path)

    features = train.drop(["Y house price of unit area", "X1 transaction date"], axis=1)
    target = train["Y house price of unit area"]

    X_train, X_test, y_train, y_test = train_test_split(
        features, target, random_state=1, test_size=0.2
    )

    return X_train, X_test, y_train, y_test


@task
def model_training_tracking(train, valid):
    def objective(params):

        with mlflow.start_run(experiment_id=1):
            # set a tag for easier classification and log the hyperparameters
            mlflow.set_tag("model", "xgboost")
            mlflow.log_params(params)

            # model definition and training
            booster = xgb.train(
                params=params,
                dtrain=train,
                num_boost_round=1000,
                evals=[(valid, "validation")],
                early_stopping_rounds=10,
            )

            # predicting with the validation set
            y_pred = booster.predict(valid)

            # rmse metric and logging
            rmse = mean_squared_error(valid.get_label(), y_pred, squared=False)
            mlflow.log_metric("rmse", rmse)

        # we return a dict with the metric and the OK signal
        return {"loss": rmse, "status": STATUS_OK}

    best_result = fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=50,
        trials=Trials(),
    )

    best_result["max_depth"] = int(best_result["max_depth"])

    return best_result


@task
def best_performing_models_production(best_result, train, valid):

    with mlflow.start_run(experiment_id=2):

        # set a tag for easier classification and log the hyperparameters
        mlflow.set_tag("model", "xgboost")
        mlflow.log_params(best_result)
        mlflow.set_tag("developer", "olamide")
        mlflow.log_param("train-data-path", "../data/train.csv")

        # model definition and training
        booster = xgb.train(
            params=best_result,
            dtrain=train,
            num_boost_round=1000,
            evals=[(valid, "validation")],
            early_stopping_rounds=50,
        )

        # predicting with the validation set
        y_pred = booster.predict(valid)

        # rmse metric and logging
        rmse = mean_squared_error(valid.get_label(), y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)

        mlflow.xgboost.log_model(booster, artifact_path="models_mlflow")

    runs = client.search_runs(
        experiment_ids="2",
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=5,
        order_by=["metrics.rmse ASC"],
    )

    model_uri = f"runs:/{runs[0].info.run_id}/model"
    mlflow.register_model(
        model_uri=model_uri,
        name=model_name,
    )

    new_stage = "Production"
    client.transition_model_version_stage(
        name=model_name, version=1, stage=new_stage, archive_existing_versions=True
    )

    return "model successfully pushed to production"


@flow(task_runner=SequentialTaskRunner())
def main(path: str = "../data/train.csv"):

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("price_prediction-training")
    mlflow.set_experiment("price_prediction-best_features")

    X_train, X_test, y_train, y_test = read_prepare_data(path).result()

    train = xgb.DMatrix(X_train, label=y_train)
    valid = xgb.DMatrix(X_test, label=y_test)

    best_result = model_training_tracking(train, valid)

    best_performing_models_production(best_result, train, valid)


main()

"""
DeploymentSpec(
    flow=main,
    name="model_training",
    schedule=IntervalSchedule(interval=timedelta(minutes=36000)),
    flow_runner=SubprocessFlowRunner(),
    tags=["mide_data_talks"]
)
"""
