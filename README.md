# molecule-django

A Django Project to make blog application Molecule

---

[TOC]

## deploy

### notable features

- .env
- mysql

## .env

```env
APPLICATION_NAME=<application_name>
ENVIRONMENT=<environment_type_string>
SECRET_KEY=<django_project_secret_key>
DEBUG=<0_or_1>
ALLOWED_HOSTS=localhost,onandgo.pythonanywhere.com,

# mysql for pythonanywhere
DATABASE_ENGINE=<pythonanywhere_mysql_engine>
DATABASE_NAME=<pythonanywhere_mysql_db_name>
DATABASE_USER=<pythonanywhere_username>
DATABASE_PASSWORD=<pythonanywhere_mysql_db_password>
DATABASE_HOST=<pythonanywhere_mysql_db_host>

# cloudinary settings
CLOUDINARY_NAME=<cloudinary_username>
CLOUDINARY_API_KEY=<cloudinary_public_api_key>
CLOUDINARY_API_SECRET=<cloudinary_secret_api_key>
```

## docker-compose.yml

```yaml
version: "3"

services:
    web:
        build: .
        command: gunicorn core.wsgi -b 0.0.0.0:8000 # gunicorn対応
        env_file: .env
        volumes:
            - .:/app
        ports:
            - 8000:8000
        depends_on:
            - db
    db:
        image: postgres:11
        volumes:
            - postgres_data:/var/lib/postgresql/data/
        environment:
            - "POSTGRES_HOST_AUTH_METHOD=trust"

volumes:
    postgres_data:
```

## test data

if you wish to set a quick data to save, feel free to use the flowing.

````markdown
# test

---

## test

### test

#### test

##### test

<article>
test
</article>

```python
print('test')
```

_test_

**test**

`test`
````
