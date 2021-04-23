FROM python:3.7-alpine
MAINTAINER Udemy Course

# print python directly
ENV PYTHONUNBUFFERED 1

# copy to docker image and run
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# create empty folder to place image and run from /app
RUN mkdir /app
WORKDIR /app
COPY ./app /app


#for jpeg. -p option will make dir if not exist
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
# create user to run for applications
RUN adduser -D user
# set ownership for user recursively
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web

USER user

