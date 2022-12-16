from django.urls import path

from . import views
from django.contrib.auth.views import LoginView


app_name = 'user'

urlpatterns = [
    path('register/', views.create_account, name="register"),
    path('login/', LoginView.as_view(template_name='./user/login.html'), name="login"),
    path('profile/', views.profile, name="profile"),
    path('checkpassword/', views.check_password_if_valid, name="checkpassword"),
    path('recoverpassword/', views.recover_password, name="recoverpassword"),
    path('changepassword/', views.change_password, name="changepassword"),
]
