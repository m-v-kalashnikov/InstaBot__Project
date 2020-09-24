# pull official base image
FROM python:3.8.5-alpine

# set work directory
RUN mkdir /code
WORKDIR /code

# adding main packages
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN pip install pipenv

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
ADD Pipfile /code/
ADD Pipfile.lock /code/
RUN set -ex && pipenv install --deploy --system

# copy(add) project
ADD . /code/