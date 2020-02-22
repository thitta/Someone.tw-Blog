#!/bin/bash

# prep
cd ~/home/someone-admin/Someone.tw-Blog &&
source venv/bin/activate;

# pull and install dependencies
git pull &&
git checkout master &&
pip install -r requirements.txt &&
deactivate;
