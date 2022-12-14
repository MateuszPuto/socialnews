from celery import Celery

app = Celery('celery_tasks', backend='rpc://', broker='amqp://rabbit:password@rabbitmq:5672//')

@app.task
def add(x, y):
    return x + y