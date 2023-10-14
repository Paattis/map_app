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

Create the first superuser by running the following command and following the on-screen instructions
```
$ docker-compose exec backend python manage.py createsuperuser
```

## Running in production mode
First you need to create an `.env.prod` file and fill it up with the relevant settings. After that you can run
```
$ docker-compose -f docker-compose.prod.yml up -d --build
```
to have the application start in production mode.


## Documentation
Documentation for the REST Api is available at the `/api/docs` endpoint

## Backend 
The backend is built with Django 

### Tests
The tests are located in the `tests/` directory of each app.

### Running tests
```
$ docker-compose exec backend python manage.py test
```

### Migrations
#### Making new migrations
```
$ docker-compose exec backend python manage.py makemigrations
```

#### Running migrations
```
$ docker-compose exec backend python manage.py migrate
```
Migrations are also run when starting up the Django application.
