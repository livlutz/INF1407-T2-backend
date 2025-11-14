#!/bin/bash

source venv/bin/activate
pip install -r requirements.txt
cd site_receitas
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
gh codespace ports visibility 8000:public