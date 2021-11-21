<p align="center">
  <img width="300px" src="https://i.pinimg.com/564x/52/af/ac/52afacaab32197c4fda199f7542732b3.jpg">
</p>

# Mokuton

Another starter template with **Django**

**Key Features**

- **RESTful API**: This template is for design purposes and rapid deployment based on the power from Django.
- **Django Ninja**: Very high performance web framework for building APIs. Thanks to **<a href="https://github.com/vitalik/django-ninja" target="_blank">vitalik
/
django-ninja</a>**
- **Very basic account authentication kit**: Forget about the initial steps from the login / registration and start racing business.
- **Preconfigured [Huey](https://github.com/coleifer/huey)**: A little task queue for python

## Installation

```
pip install -r requirements.txt
```



## Usage

### Migrate database

```
python manage.py makemigrations

python manage.py migrate
```

### Run server

```
python manage.py runserver
```

### Create superuser for the first run

```
python manage.py createsuperuser
```

### Interactive API docs

Now go to <a href="http://127.0.0.1:8000/api/docs" target="_blank">http://127.0.0.1:8000/api/docs</a>

You will see the automatic interactive API documentation (provided by <a href="https://github.com/swagger-api/swagger-ui" target="_blank">Swagger UI</a>):

### Huey task queue

In one terminal, run:

```
python manage.py run_huey
```
