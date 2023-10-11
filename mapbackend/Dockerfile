FROM python:3.11-slim

WORKDIR /src/backend/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update
#RUN apt-get install sudo
RUN apt-get install binutils libproj-dev gdal-bin -y


COPY . .
