FROM python:3.6.9-slim-buster

WORKDIR /opt/app
COPY . /opt/app

ENTRYPOINT ["python", "main.py"]