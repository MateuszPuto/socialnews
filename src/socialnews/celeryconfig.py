BROKER_HOST = "rabbitmq"
BROKER_PORT = 5672
BROKER_USER = "rabbitmq"
BROKER_PASSWORD = "rabbitmq"
BROKER_VHOST = "my_vhost"

CELERY_RESULT_BACKEND = "rpc://"
CELERY_BROKER_URL="amqp://rabbitmq:rabbitmq@rabbitmq:5672/my_vhost"

CELERY_IMPORTS = ("socialnews.tasks", "math")