FROM python:3.11-bullseye
WORKDIR .

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY /src /src
