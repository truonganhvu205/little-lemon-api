# Create a Django Project using pipenv
## Install pipenv
```bash
pip3 install pipenv
```

```bash
mkdir littlelemonAPI

cd littlelemonAPI
```

## Install Django
```bash
pipenv install django
```

## Activate virtual environment
```bash
pipenv shell
```

## Create Django project
```bash
django-admin startproject LittleLemon .
```

## Create Django app
```bash
python3 manage.py startapp LittleLemonAPI
```

# Install Framework
```bash
pipenv install djangorestframework
pipenv install django-debug-toolbar
pipenv install djangorestframework-xml
pipenv install bleach
pipenv install django-filter
```

# Run server
```bash
python3 manage.py runserver
```