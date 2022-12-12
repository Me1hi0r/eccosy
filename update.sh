#!/bin/bash/env bash
echo "update src, static, deps and migrate for prod server"
git pull
source ~/app/eccosy/env/bin/activate
pip install -r req/requirements.in
python src/manage.py collectstatic --noinput
python src/manage.py migrate
sudo systemctl restart eccosy
