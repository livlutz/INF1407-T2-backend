#!/bin/bash

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd site_receitas
python manage.py makemigrations
python manage.py migrate
python manage.py runserver