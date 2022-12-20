# Create your tasks here
from celery import shared_task


@shared_task
def add_nums(x, y):
    return x + y


@shared_task
def mul_nums(x, y):
    return x * y


@shared_task
def xsum_nums(numbers):
    return sum(numbers)