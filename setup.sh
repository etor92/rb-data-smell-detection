#!/bin/bash

# Check if virtualenv is installed
if ! command -v virtualenv &> /dev/null
then
    echo "virtualenv could not be found, please install it first."
    exit 1
fi

# Create and activate the virtual environment
virtualenv env
source env/bin/activate

# Change directory to data_smell_detection and install dependencies
cd data_smell_detection && pwd
pip install -r requirements-dev.in
python3 setup.py install

# Navigate to the Django project directory and set it up
cd ../web_application/argon-dashboard-django/
pip3 install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
