# pull official base image
FROM python:3.8.5-alpine

# set work directory
RUN mkdir /code
WORKDIR /code

# adding main packages
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libjpeg gettext
RUN pip install --upgrade pip
RUN pip install pipenv
#RUN pipenv install Pillow

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
ADD Pipfile* /code/
RUN set -ex && pipenv install --deploy --system

# copy(add) script
COPY ./insta_bot_api/scripts/start.sh /

# copy(add) project
ADD . /code/