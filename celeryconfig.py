## Broker settings.
broker_url = 'amqp://rabbit:password@rabbitmq:5672//'

# List of modules to import when the Celery worker starts.
imports = ('celery_tasks',)