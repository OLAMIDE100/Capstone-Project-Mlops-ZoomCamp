import requests

house = {
    "X2 house age": 31.0,
    "X3 distance to the nearest MRT station": 1156.412,
    "X4 number of convenience stores": 0.0,
    "X5 latitude": 24.9489,
    "X6 longitude": 121.53095,
}

url = "http://127.0.0.1:9696/predict"
response = requests.post(url, json=house)
print(response.json())
