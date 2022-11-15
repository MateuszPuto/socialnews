from django import forms

class NewTopic(forms.Form):
    title = forms.CharField(label="title", max_length=100)
    content = forms.CharField(label="content", max_length=500)

class NewComment(forms.Form):
    content = forms.CharField(label="content", max_length=200)
