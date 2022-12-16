from django.db import models
import uuid

from django.contrib.auth.models import User


class Topic(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    content = models.CharField(max_length=500)
    pub_date = models.DateTimeField('publish date')
    votes = models.IntegerField(default=0)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Comment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.content

class VotedPosts(models.Model):
    username = models.CharField(max_length=50)
    voted = models.UUIDField(editable=True)

class VotedComments(models.Model):
    username = models.CharField(max_length=50)
    voted = models.UUIDField(editable=True)
