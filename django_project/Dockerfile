FROM python:3.8-slim-buster

WORKDIR /app

ADD requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ADD . . 

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 