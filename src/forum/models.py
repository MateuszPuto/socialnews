from django.db import models

class Topic(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    content = models.CharField(max_length=500)
    pub_date = models.DateTimeField('publish date')
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.content