FROM python:2.7-alpine
RUN mkdir /code
RUN apk add mariadb-dev  gcc linux-headers musl-dev mariadb-connector-c libffi-dev
RUN pip install mysqlclient==1.4.2.post1
WORKDIR /code
