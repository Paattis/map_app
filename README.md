# Basic social map application example

## Setting up a dev environment

Create a .env file using the template provided
```
# Linux/MacOS/Other Unix-like OS
$ cp .env.template .env
# Windows
$ copy .env.template .env
```
and then fill out the sensitive details in the .env file.

Build and run the entire stack with
```
$ docker-compose up -d --build
```

Run the migrations
```
$ docker-compose exec backend python manage.py migrate
```

Create the first superuser by running the following command and following the on-screen instructions
```
$ docker-compose exec backend python manage.py createsuperuser
```

## Documentation
Documentation for the REST Api is available at the `/docs` endpoint

### Backend 
The backend is built with Django 

#### Migrations
To make new migrations
```
$ docker-compose exec backend python manage.py makemigrations
```

To run migrations
```
$ docker-compose exec backend python manage.py migrate
```
