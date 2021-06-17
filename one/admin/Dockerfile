FROM python:3.8.5

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]