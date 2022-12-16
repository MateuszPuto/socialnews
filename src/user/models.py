from django.db import models

class Secrets(models.Model):
    username = models.CharField(max_length=50)
    secret = models.IntegerField()
