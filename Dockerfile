FROM python:3

ENV VERSION=1
ENV POSTGRES_USER user
ENV POSTGRES_DB database
ENV POSTGRES_PASSWORD password
ENV POSTGRES_HOST example.com
ENV TON_SERVICE_BASE_URL http://example.com/api


WORKDIR /app


RUN apt-get update && apt-get upgrade -y \
    && apt-get -y install netcat gcc \
    && apt-get clean


RUN pip install --upgrade pip

COPY ./requirements.txt ./app
COPY ./ ./

RUN pip install -r requirements.txt