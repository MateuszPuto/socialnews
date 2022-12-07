from django.urls import path

from . import views
from django.contrib.auth.views import LoginView


app_name = 'forum'
urlpatterns = [
        path('<slug:post_uuid>/', views.post, name="post"),
        path('register/', views.create_account, name="register"),
        path('login/', LoginView.as_view(template_name='login.html'), name="login"),
        path('profile/', views.profile, name="profile"),
        path('checkpassword/', views.check_password_if_valid, name="checkpassword"),
        path('comment/<slug:post_uuid>/', views.comment, name="newcomment"),
        path('addlike/<slug:comment_uuid>', views.likeit, name="addlike"),
        path('index.html/', views.index, name='index'),   
        path('newpost.html/', views.addtopic, name="newpost"),
        path('', views.index),
    ]


