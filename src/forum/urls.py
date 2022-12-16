from django.urls import path

from . import views
from django.contrib.auth.views import LoginView


app_name = 'forum'
urlpatterns = [
        path('comment/<slug:post_uuid>/', views.comment, name="newcomment"),
        path('addlike/<slug:comment_uuid>', views.likeit, name="addlike"),
        path('voteit/<slug:post_uuid>', views.voteit, name="vote"),
        path('index.html/', views.index, name="index"),
        path('feed.html/', views.feed, name="feed"),
        path('newest.html/', views.newest, name="newest"),
        path('local.html/', views.local, name="local"),
        path('newpost.html/', views.addtopic, name="newpost"),
        path('<slug:post_uuid>/', views.post, name="post"),
        path('', views.index),
    ]
