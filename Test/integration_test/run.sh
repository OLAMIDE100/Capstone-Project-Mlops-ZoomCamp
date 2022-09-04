#!/usr/bin/env bash

cd web*


docker-compose up  -d

sleep 10

pipenv run python test.py


ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose down
    exit ${ERROR_CODE}
fi


docker-compose down
