#!/bin/bash

# prep
cd /home/someone-admin/Someone.tw-Blog &&
source venv/bin/activate;

# reset nginx file
sudo rm /etc/nginx/sites-available/someone &&
sudo rm /etc/nginx/sites-enabled/someone &&
sudo mv ~/Someone.tw-Blog/bash/ubuntu/someone-nginx_setting /etc/nginx/sites-available/someone &&
sudo ln -s /etc/nginx/sites-available/someone /etc/nginx/sites-enabled &&

# restart nginx
sudo systemctl restart nginx &&
sudo nginx -t ;