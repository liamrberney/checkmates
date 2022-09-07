from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    profile_picture = forms.FileField()
    phone = forms.CharField()
    email = forms.CharField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture', 'email','phone', 'username','password1','password2']

