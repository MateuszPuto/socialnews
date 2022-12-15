from celery import Celery
import os

app = Celery('celery_tasks', broker=os.environ['CELERY_BROKER'])

@app.task
def add(x, y):
    return x + y
