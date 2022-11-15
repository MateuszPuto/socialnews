from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
        path('<int:post_id>/', views.post),
        path('comment/<int:post_id>/', views.comment, name="newcomment"),
        path('index.html/', views.index, name='index'),   
        path('newpost.html/', views.addtopic, name="newpost"),
        path('', views.index),
    ]
