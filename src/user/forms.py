from django import forms
from django.core.validators import validate_slug, validate_email

class CreateAccount(forms.Form):
    username = forms.SlugField(max_length=30, validators=[validate_slug])
    email = forms.EmailField(validators=[validate_email])
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

class CheckPassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

class ChangePassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    secret = forms.IntegerField(max_value=9999)
