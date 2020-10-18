#!/bin/bash
source /home/dalex/code/django_web_scraping/venv/bin/activate
exec gunicorn  -c "/home/dalex/code/django_web_scraping/gunicorn_config.py" django_web_scraping.wsgi
