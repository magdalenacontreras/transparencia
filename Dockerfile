FROM python:2.7-alpine
RUN mkdir /code
RUN apk add mariadb-dev 
RUN pip install --no-cache-dir MySQL-python==1.2.3rc1
WORKDIR /code
