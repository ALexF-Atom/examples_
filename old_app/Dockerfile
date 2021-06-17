FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD ./requirements/docker.txt /code/requirements/
RUN /usr/local/bin/python -m pip install --upgrade pip; pip install -r /code/requirements/docker.txt
ADD . /code/
