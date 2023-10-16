FROM python:3.11-slim

WORKDIR /src/backend/
RUN mkdir /src/backend/staticfiles

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN chmod +x /src/backend/entrypoint.sh
COPY ./entrypoint.prod.sh .
RUN chmod +x /src/backend/entrypoint.prod.sh

# install dependencies for PostGIS
RUN apt-get update
RUN apt-get install binutils libproj-dev gdal-bin -y

COPY . .


