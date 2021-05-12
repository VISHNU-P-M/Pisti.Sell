# API for ZIP_CODES.csv

Here you have two APIs for getting all fields of an zipcodes.csv file, creating new row to file, getting specific datas of an zip code, and updating population of that specific zip code.
#### Call 'api/zip-codes' GET API for get all zip code datas
#### Call 'api/data/<ZIP_CODE>' GET API for get specific zip code datas 
#### Call 'api/data/<ZIP_CODE>' PUT API for updating population of that specific zip code
#### Call 'api/data/<ZIP_CODE>' POST API for add new row in file of zip codes

## Creating Environment

Create an environment on your system

```bash
Install virtual environment:
python -m pip install --user virtualenv

Creating new environment:
py -m venv env

Activate environment:
.\env\Scripts\activate
```

## Install all requirments

Install all package that needs to run this application

```bash
pip install requirements.txt 
```

## Run Application
First you need to migrate, collect static files, and then Run

```bash
python manage.py migrate

python manage.py collectstatic

python manage.py runserver
```
