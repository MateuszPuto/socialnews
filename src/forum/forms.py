from django import forms
from django.core.validators import validate_slug, validate_email

class NewTopic(forms.Form):
    title = forms.CharField(label="title", max_length=100)
    url = forms.URLField(label="url", max_length=200)
    content = forms.CharField(label="content", max_length=500)

class NewComment(forms.Form):
    content = forms.CharField(label="content", max_length=200)

class CreateAccount(forms.Form):
    username = forms.SlugField(max_length=30, validators=[validate_slug])
    email = forms.EmailField(validators=[validate_email])
    password = forms.CharField(widget=forms.PasswordInput)

class CheckPassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
