# Capstone Project (Mlops-Zoomcamp) - House Price Prediction

![Architecture](./imgs/project_architecture.png)

## Problem Statement

This is a capstone project associated with [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp), and it will be peer reviewed and scored.

The end goal of the project is to build an end-to-end machine learning project containing feature engineering, trainig, vallidation,tracking, modeel deployment,hosting and general engineering best practices aimed at making house price prediction.


## Dataset

This  data set has 414 rows and 7 columns. 
It provides the market historical data set of real estate valuations which are collected from Sindian Dist., New Taipei City, Taiwan.
This data set is recommended for learning and practicing your skills in **exploratory data analysis**, **data visualization**, and **regression modelling techniques**. 
Feel free to explore the data set with multiple **supervised** and **unsupervised** learning techniques. 
The Following data dictionary gives more details on this data set:

---

### Data Dictionary 

| Column   Position 	| Atrribute Name                         	| Definition                                                                                                                                                                 	| Data Type    	| Example                         	| % Null Ratios 	|
|-------------------	|----------------------------------------	|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|--------------	|---------------------------------	|---------------	|
| 1                 	| X1 transaction date                    	| The   transaction date (for example, 2013.250=2013 March, 2013.500=2013 June, etc.)                                                                                        	| Qualitative  	| 2013.500,   2013.500, 2013.333  	| 0             	|
| 2                 	| X2 house age                           	| The house age   (unit: year)                                                                                                                                               	| Quantitative 	| 19.5, 13.3, 5.0                 	| 0             	|
| 3                 	| X3 distance to the nearest MRT station 	| The distance   to the nearest MRT station (unit: meter)                                                                                                                    	| Quantitative 	| 390.5684, 405.21340, 23.38284   	| 0             	|
| 4                 	| X4 number of convenience stores        	| The number of   convenience stores in the living circle on foot                                                                                                            	| Quantitative 	| 6, 8, 1                         	| 0             	|
| 5                 	| X5 latitude                            	| The geographic   coordinate, latitude (unit: degree)                                                                                                                       	| Quantitative 	| 24.97937,   24.97544, 24.94925  	| 0             	|
| 6                 	| X6 longtitude                          	| The geographic   coordinate, longitude (unit: degree)                                                                                                                      	| Quantitative 	| 121.54243, 121.49587, 121.51151	 	| 0             	|
| 7                 	| Y house price of unit area             	| The house price of unit   area (10000 New Taiwan Dollar/Ping, where Ping is a local unit, 1 Ping = 3.3   meter squared) for example, 29.3 = 293,000 New Taiwan Dollar/Ping 	| Quantitative 	| 29.3, 33.6, 47.7


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

