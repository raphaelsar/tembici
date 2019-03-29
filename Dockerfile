FROM python:3.7.2-alpine3.8

MAINTAINER Raphael Ramos <saponeis@gmail.com>
LABEL version="1.0.0"


RUN apk add --no-cache --update bash build-base
RUN apk add --no-cache libffi-dev gcc


RUN mkdir src
WORKDIR src

ADD app ./app
ADD logger ./logger
ADD Makefile .
ADD requirements.txt .
ADD index.py .
ADD config.py .

RUN pip install -U pip setuptools
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python","index.py"]