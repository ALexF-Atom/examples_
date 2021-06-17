FROM python:3.8.5

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

ADD requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip; pip install -r requirements.txt

ADD . .

EXPOSE 8000