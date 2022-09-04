import os
import time

import numpy
import mlflow
import pandas as pd
from dotenv import load_dotenv
from mlflow.tracking import MlflowClient

load_dotenv()


TRACKING_SERVER_HOST = os.getenv("AWS_EC2_PEUBLIC_DNS")
MLFLOW_TRACKING_URI = f"http://{TRACKING_SERVER_HOST}:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)


latest_versions = client.get_latest_versions(name="house-price-regressor")[0].run_id

PATH = "../data/batch_test.csv"


train = pd.read_csv(PATH)

features = train.drop(["Y house price of unit area", "X1 transaction date"], axis=1)


target = train["Y house price of unit area"]


model = mlflow.pyfunc.load_model(f"runs:/{latest_versions}/models_mlflow")


for row, tar in zip(features.values, target):
    fv = numpy.array(row).reshape((1, -1))
    y_pred = model.predict(fv)

    print(y_pred, tar)

    time.sleep(1)
