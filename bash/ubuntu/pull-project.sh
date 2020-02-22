#!/bin/bash

# prep
cd ~/home/someone-admin/Someone.tw-Blog;

# pull
git pull;
git checkout master;

# install dependencies
source venv/bin/activate;
pip install -r requirements.txt;
deactivate;
