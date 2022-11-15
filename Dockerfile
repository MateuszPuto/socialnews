FROM python:3.9
WORKDIR src
COPY pyproject.toml .
RUN pip3 install poetry
RUN poetry install
EXPOSE 8000
COPY . .
