# Basic social map application example

## Installation

Create a .env file using the template provided
```
# Linux/MacOS/Other Unix-like OS
$ cp .env.template .env
# Windows
$ copy .env.template .env
```
and then fill out the sensitive details in the .env file.

### Backend
The backend is built with django.


#### Running
To build and run
```
$ docker-compose up -d --build
```

#### Migrations

Make migrations with
```
$ docker-compose exec backend python manage.py makemigrations
```

To run the migrations with
```
$ docker-compose exec backend python manage.py migrate
```