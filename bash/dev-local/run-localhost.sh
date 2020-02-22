#!/bin/bash

source ~/PycharmProjects/someone_blog/bash/dev-local/init.sh;

# select config/db
export DJANGO_SETTINGS_MODULE="settings.core";
export SOMEONE_USE_PROD_CFG="FALSE";
export SOMEONE_USE_PROD_DB="FALSE";

# run
python manage.py runserver;