
from django import forms
from app.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=50, required=True)    

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]
    

