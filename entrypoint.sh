#!/bin/sh
set -e
service ssh start
#exec python manage.py migrate 
#exec python manage.py runserver 0.0.0.0:80
tail -f /dev/null