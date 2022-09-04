import os

import numpy as np
from dotenv import load_dotenv

load_dotenv()


import mlflow
import requests
from flask import Flask, jsonify, request
from pymongo import MongoClient
from mlflow.tracking import MlflowClient

TRACKING_SERVER_HOST = os.getenv("AWS_EC2_PEUBLIC_DNS")
MLFLOW_TRACKING_URI = f"http://{TRACKING_SERVER_HOST}:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)


latest_versions = client.get_latest_versions(name="house-price-regressor")[0].run_id


model = mlflow.pyfunc.load_model(f"runs:/{latest_versions}/models_mlflow")


EVIDENTLY_SERVICE_ADDRESS = os.getenv("EVIDENTLY_SERVICE", "http://127.0.0.1:5000")
MONGODB_ADDRESS = os.getenv("MONGODB_ADDRESS", "mongodb://127.0.0.1:27017")


app = Flask("house_price")
mongo_client = MongoClient(MONGODB_ADDRESS)
db = mongo_client.get_database("prediction_service")
collection = db.get_collection("data")


def save_to_db(record, prediction):
    rec = record.copy()
    rec["prediction"] = prediction
    collection.insert_one(rec)


def send_to_evidently_service(record, prediction):
    rec = record.copy()
    rec["prediction"] = prediction
    requests.post(f"{EVIDENTLY_SERVICE_ADDRESS}/iterate/taxi", json=[rec])


def predict_(house):

    features = np.array(list(house.values())).reshape((1, -1))

    preds = model.predict(features)
    return float(preds[0])


@app.route("/predict", methods=["POST"])
def predict():

    house = request.get_json()

    pred = predict_(house)

    result = {"price": pred, "version": latest_versions}

    save_to_db(house, float(pred))
    send_to_evidently_service(house, float(pred))
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)
