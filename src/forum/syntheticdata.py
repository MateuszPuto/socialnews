import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "socialnews.settings")

import django
django.setup()

import string

import read_bbc_dataset

from socialnews.tasks import classify_text 

from faker import Faker
from random import randrange
from forum.models import Topic, Comment, Location

def populate_models():
    Faker.seed(0)
    fake = Faker()

    itrs = read_bbc_dataset.get_genre_iterators('..')
    curr_itr = 0

    for i in range(0, 100):
        article = itrs[curr_itr].read_news()
        curr_itr = (curr_itr + 1) % len(itrs)

        article_title = article[0]
        article_content = article[1][:500].rstrip(string.printable.replace('.', ''))

        topic = Topic.objects.create(
            username = fake.first_name() + fake.last_name(),
            pub_date = fake.date_this_month(),
            url = fake.uri(),
            title = article_title,
            content = article_content,
            votes = randrange(0, 100),
            geography = bool(randrange(0, 2))
        )

        text = article_title + ". " + article_content
        classify_text.apply_async(args=[topic.uuid, text], countdown=20*(i+1))

        if topic.geography == True:
            place = fake.location_on_land()

            location = Location.objects.create(
                relates = topic,
                latitude = place[0],
                longitude = place[1],
            )


    objects = Topic.objects.all()
    for obj in objects:
        for i in range(0, 5):
            comment = Comment.objects.create(
                topic=obj,
                content=fake.sentence(),
                votes=randrange(0,20),
                username=fake.first_name() + fake.last_name(),
            )