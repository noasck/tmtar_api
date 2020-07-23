FROM python:3.6.11-slim-buster

WORKDIR /usr/src/tmtart

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/tmtart/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/tmtart/