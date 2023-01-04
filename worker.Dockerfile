FROM python:3.11-alpine
WORKDIR .

COPY ./requirements.txt .

RUN apk add python3-dev py3-numpy build-base
RUN pip install -r requirements.txt

COPY . .
