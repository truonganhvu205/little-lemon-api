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

# API endpoints
```bash
/auth/users
/auth/users/me/
/auth/token/login/ OR api/api-token-auth/
```

## Menu-items endpoints
```bash
/api/menu-items
/api/menu-items/<int:pk>
```

## User group management endpoints
```bash
/api/groups/manager/users
/api/groups/manager/users/<int:pk>
```

```bash
/api/groups/delivery-crew/users
/api/groups/delivery-crew/users/<int:pk>
```

## Cart management endpoints
```bash
/api/cart/menu-items
```

## Order management endpoints
```bash
/api/orders
/api/orders/<int:pk>
```
