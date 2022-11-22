FROM python:3.9
EXPOSE 8000
WORKDIR /src
RUN apt-get update && apt-get -y install libpq-dev gcc
COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

COPY /src .
CMD ./manage.py runserver --insecure 0.0.0.0:8000