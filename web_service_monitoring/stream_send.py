from time import sleep

import pandas as pd
import requests

path = "../data/train.csv"

train = pd.read_csv(path)

features = train.drop(["Y house price of unit area", "X1 transaction date"], axis=1)

features = features.to_dict("records")

for row in features:

    url = "http://127.0.0.1:9696/predict"
    response = requests.post(url, json=row)
    print(response.json())
    sleep(1)
