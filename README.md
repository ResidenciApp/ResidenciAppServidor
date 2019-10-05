# ResidenciApp Servidor Django

### Dependencias

```console
$ pip install djangorestframework
$ pip install Django
$ pip install psycopg2
```

### Crear una App
```console
$ cd Apps/
$ django-admin startapp nombre_de_la_app
```

### Hacer Migraciones

```console
$ python manage.py migrate
$ python manage.py makemigrations
```

### Crear un Super Usuario
```console
$ python manage.py createsuperuser
```