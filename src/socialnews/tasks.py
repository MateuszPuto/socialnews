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

@shared_task
def haversine_distance(point, point2):
    import math
    '''Used to calculate distance between two polar coordinate points on a sphere'''
    lat, long = point
    lat2, long2 = point2

    lat = math.radians(lat)
    long = math.radians(long)
    lat2 = math.radians(lat2)
    long2 = math.radians(long2)

    a = math.pow(math.sin(abs(lat - lat2)) / 2, 2) + math.cos(lat) * math.cos(lat2) *  math.pow(math.sin(abs(long - long2)) / 2, 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371
    
    return R * c

    