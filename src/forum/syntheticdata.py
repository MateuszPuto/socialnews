import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "socialnews.settings")

import django
django.setup()

from faker import Faker
from random import randrange
from forum.models import Topic, Comment

Faker.seed(0)
fake = Faker()

for _ in range(0, 100):
    topic = Topic.objects.create(
        username = fake.first_name() + fake.last_name(),
        pub_date = fake.date_this_month(),
        url = fake.uri(),
        title = " ".join(fake.words()),
        content = fake.paragraph(nb_sentences=3),
        votes = randrange(0, 100),
    )

    topic.save()

objects = Topic.objects.all()
for obj in objects:
    for i in range(0, 5):
        comment = Comment.objects.create(
            topic=obj,
            content=fake.sentence(),
            votes=randrange(0,20),
            username=fake.first_name() + fake.last_name(),
        )

    comment.save()