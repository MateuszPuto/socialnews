from django.urls import path

from . import views
from django.contrib.auth.views import LoginView


app_name = 'forum'
urlpatterns = [
        path('<int:post_id>/', views.post),
        path('register/', views.create_account, name="register"),
        path('login/', LoginView.as_view(template_name='login.html'), name="login"),
        path('comment/<int:post_id>/', views.comment, name="newcomment"),
        path('index.html/', views.index, name='index'),   
        path('newpost.html/', views.addtopic, name="newpost"),
        path('', views.index),
    ]


