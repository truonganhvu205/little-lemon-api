# Clone project
```bash
mkdir littlelemonAPI

cd littlelemonAPI

git init

git clone https://github.com/truonganhvu205/little-lemon-API.git
```

## Install pipenv
```bash
pip3 install pipenv
```

## Activate virtual environment
```bash
pipenv --python 3.10
pipenv shell
```

## Install Django
```bash
pipenv install django
```

## Create Django project
```bash
django-admin startproject LittleLemon .
```

## Create Django app
```bash
python3 manage.py startapp LittleLemonAPI
```

## Install Framework
```bash
pipenv install djangorestframework
pipenv install django-debug-toolbar
# pipenv install djangorestframework-xml
pipenv install bleach
pipenv install djoser
# pipenv install djangorestframework-simplejwt
```

# Run server
```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
