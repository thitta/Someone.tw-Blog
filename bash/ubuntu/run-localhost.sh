#!/bin/bash

# prep
cd /home/someone-admin/Someone.tw-Blog;
source venv/bin/activate;

# main
export DJANGO_SETTINGS_MODULE="settings.core" &&
export SOMEONE_USE_PROD_CFG="FALSE" &&
export SOMEONE_USE_PROD_DB="FALSE" &&
python manage.py runserver;