#!/bin/sh
set -e
echo $environment > .env
service ssh start
python manage.py makemigrations
python manage.py migrate 
exec python manage.py runserver 0.0.0.0:80
#tail -f /dev/null