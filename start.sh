#!/bin/bash/env bash
echo "start eccosy prodaction server"
source /home/admin/app/eccosy/env/bin/activate
gunicorn -c /home/admin/app/eccosy/src/config/gunicorn_config.py config.wsgi
