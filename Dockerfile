FROM python:3.7-alpine
MAINTAINER Udemy Course

# print python directly
ENV PYTHONUNBUFFERED 1

# copy to docker image and run
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# create empty folder to place image and run from /app
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# create user to run for applications
RUN adduser -D user
USER user

