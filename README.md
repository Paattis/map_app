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

By default the backend should be available at `http://localhost/8000/api` and the frontend at `http://localhost:3000`.

### Initial data

When running in development mode the application has some data pre-loaded as well as some users. With the following username-password pairs.

| username         | password |
| ---------------- | -------- |
| MattiMeikalainen | password |
| TeuvoTestaaja    | password |

## Running in production mode

First you need to create an `.env.prod` file and fill it up with the relevant settings. After that you can run

```
$ docker-compose -f docker-compose.prod.yml up -d --build
```

to have the application start in production mode.

## Documentation

### Documentation page

Documentation for the REST Api is available at the `/api/docs` endpoint. Its accessible with a superuser account.

## Admin page

Admin page for the Django backend is available at the `/api/admin/` endpoint.

## Backend

The backend is built with Django using the Django Rest Framework library.

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

## Frontend

The frontend is a fairly basic React+TypeScript application.

### Running in development mode

For faster development iterations it may be useful to run the development server without docker (while running the database and backend services with it, of course).

```
# only start up the Django and PostreSQL services with Docker
$ docker-compose up backend db

# install dependencies
$ npm install
# start up Node development server
$ npm start
```
