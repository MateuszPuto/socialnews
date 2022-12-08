from django.urls import path

from . import views
from django.contrib.auth.views import LoginView


app_name = 'forum'
urlpatterns = [
        path('register/', views.create_account, name="register"),
        path('login/', LoginView.as_view(template_name='login.html'), name="login"),
        path('profile/', views.profile, name="profile"),
        path('checkpassword/', views.check_password_if_valid, name="checkpassword"),
        path('recoverpassword/', views.recover_password, name="recoverpassword"),
        path('changepassword/', views.change_password, name="changepassword"),
        path('comment/<slug:post_uuid>/', views.comment, name="newcomment"),
        path('addlike/<slug:comment_uuid>', views.likeit, name="addlike"),
        path('voteit/<slug:post_uuid>', views.voteit, name="vote"),
        path('index.html/', views.index, name='index'),   
        path('newpost.html/', views.addtopic, name="newpost"),
        path('<slug:post_uuid>/', views.post, name="post"),
        path('', views.index),
    ]


