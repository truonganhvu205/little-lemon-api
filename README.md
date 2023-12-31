# Clone project
```bash
git init
git clone https://github.com/truonganhvu205/little-lemon-api.git
cd little-lemon-api
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

## Install Django & frameworks
```bash
# Django
pipenv install django

# Frameworks
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
## Account required
```bash
Admin
    admin
    adminuser123$%^

Delivery crew
    johndoe
    johndoeuser123$%^

Manager
    janedoe
    janedoeuser123$%^

Customer
    babydoe
    babydoeuser123$%^
```

```bash
/auth/users
/auth/users/me/
/auth/token/login/
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

## Deactivate virtual environment
```bash
exit
```