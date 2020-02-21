#!/bin/bash

cd ~/PycharmProjects/someone_blog

SOMEONE_USE_PROD_CFG="FALSE"
SOMEONE_USE_PROD_DB="FALSE"

python ./manage.py test tests/*/ --pattern="test_*.py"
