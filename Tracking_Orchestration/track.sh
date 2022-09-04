#!/usr/bin/env bash

cd Track*


pipenv run python train.py

pipenv run python test.py
