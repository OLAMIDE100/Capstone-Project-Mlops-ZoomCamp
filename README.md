# Capstone Project (Mlops-Zoomcamp) - House Price Prediction

![Architecture](./imgs/project_architecture.png)

## Problem Statement

This is capstone project associated with [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp), and it will be peer reviewed and scored.

The end goal of the project is to build an end-to-end machine learning project containing feature engineering, trainig, vallidation,tracking, modeel deployment,hosting and general engineering best practices aimed at making house price prediction.


## Dataset

This project gets data from [Kaggle](https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data) and creates a model to predict the list price of vehicles on Craiglist.
This predicted value can help users to understand how much a vehicle is worth. For that, users can use a web app to input the characteristics of the given vehicle.


## System architecture and Technologies

The following figure depicts the system architecture:

![Architecture](./imgs/project_architecture.png)

The main technologies are the following ones:
* Cloud: AWS
* Experiment tracking and model registry: MLFlow
* Container: Docker + Docker Compose
* Infrastructure as code (IaC): Terraform
* Workflow orchestration: Airflow
* Storage: S3
* Monitoring: Evidently
* Web app: Flask + Gunicorn + Streamlit
* CI/CD: GitHub actions
* Linter and code formaters: Pylint + Black + isort


## Flow

Airflow orchestrates the download of the dataset from Kaggle, the modeling and deployment of the initial model, by using MLFlow for experiment tracking and model registry. The model is set to production stage. 
XGBoost is used for creating the model.
Some other tasks run in the background to guarantee that the entire service will run smoothly when started.

When the service boots, it obtains the model staged in production from MLFlow, starts the Flask app and Gunicorn for serving web requests, starts Evidently for monitoring the data input by the user, and starts Streamlit for the frontend, where the user can predict values for vehicles. 

Whenever the ratio of variables drifting passes a pre-defined threshold, it triggers alerts to the user. Meanwhile, drift reports can be observed using Grafana.

More info on the flow can be found [here](./setup/flow.md).


## Setup

This project has as main pre-requisites:
* AWS account
* Terraform
* Docker and Docker Compose

For more info on how to setup this architecture and run the code please check the following documentation:

1. [setup_aws_mlflow.md](./setup/setup_aws_mlflow.md)
2. [setup_kaggle.md](./setup/setup_kaggle.md)
3. [setup_terraform.md](./setup/setup_terraform.md)
4. [setup_env.md](./setup/setup_env.md)

You can run the project using:
```
make build
```


## Project Tree Structure

The following is the resulting repo structure:

    .
|-- Makefile
|-- README.md
|-- Test
|   `-- integration_test
|       `-- run.sh
|-- Tracking_Orchestration
|   |-- Pipfile
|   |-- Pipfile.lock
|   |-- test.py
|   |-- track.sh
|   `-- train.py
|-- data
|   |-- batch_test.csv
|   |-- data.xlsx
|   `-- train.csv
|-- images
|   |-- MLFLOW_EXPER.PNG
|   |-- deploy.PNG
|   |-- docker.PNG
|   |-- drift.PNG
|   |-- mlflow_model.PNG
|   |-- train.PNG
|   `-- web_page_STREAMLIT.PNG
|-- pyproject.toml
|-- streamlit
|   |-- Dockerfile
|   |-- Pipfile
|   |-- Pipfile.lock
|   |-- frontend.py
|   `-- images
|       `-- house.jpg
`-- web_service_monitoring
    |-- Pipfile
    |-- Pipfile.lock
    |-- docker-compose.yml
    |-- evidently_service
    |   |-- Dockerfile
    |   |-- app.py
    |   |-- config
    |   |   |-- grafana_dashboards.yaml
    |   |   |-- grafana_datasources.yaml
    |   |   `-- prometheus.yml
    |   |-- config.yaml
    |   |-- dashboards
    |   |   |-- cat_target_drift.json
    |   |   |-- classification_performance.json
    |   |   |-- data_drift.json
    |   |   |-- num_target_drift.json
    |   |   `-- regression_performance.json
    |   |-- datasets
    |   |   `-- train.csv
    |   `-- requirements.txt
    |-- prediction_service
    |   |-- Dockerfile
    |   |-- app.py
    |   `-- requirements.txt
    |-- requirements.txt
    |-- stream_send.py
    `-- test.py

13 directories, 46 files

