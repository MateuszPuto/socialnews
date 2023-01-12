from django.contrib import admin
from forum.models import Topic, Comment, About

admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(About)