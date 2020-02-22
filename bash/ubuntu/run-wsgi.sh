#!/bin/bash

# prep
cd /home/someone-admin/Someone.tw-Blog &&
source venv/bin/activate;

# init gunicorn
export DJANGO_SETTINGS_MODULE="settings.core" &&
export SOMEONE_USE_PROD_CFG="FALSE" &&
export SOMEONE_USE_PROD_DB="FALSE";

gunicorn --access-logfile - \
         --workers        5 \
         --bind           unix:/home/someone-admin/Someone.tw-Blog/wsgi.sock \
         wsgi:application \
;
