FROM python:3.9-alpine
EXPOSE 8000
WORKDIR /src
RUN --mount=type=cache,target=/var/cache/apk  \
    ln -vs /var/cache/apk /etc/apk/cache && \
	apk add --update gcc build-base
ENV PIP_CACHE_DIR=/var/cache/pip

# If this is set to a non-empty string, Python won’t try to write .pyc files on the import of source modules. This is equivalent to specifying the -B option.
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
ENV PYTHONDONTWRITEBYTECODE 1

# If this is set to a non-empty string it is equivalent to specifying the -u option.
# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN --mount=type=cache,target=$PIP_CACHE_DIR \
    pip install -r requirements.txt && \
    rm requirements.txt

COPY /src .
CMD ./manage.py runserver --insecure 0.0.0.0:8000
