FROM python:3.10-alpine3.16

ENV PIP_ROOT_USER_ACTION=ignore

RUN mkdir /jwt-auth

WORKDIR /jwt-auth 

ADD . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt