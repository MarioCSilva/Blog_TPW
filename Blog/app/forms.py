
from django import forms
from app.models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=50, required=True,widget=forms.TextInput(attrs={'placeholder':'Email'}))
    username = forms.CharField(max_length=50,required=True,widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password1 =  forms.CharField(min_length=5,max_length=50,required=True,widget=forms.TextInput(attrs={'placeholder':'Password'}))
    password2 =  forms.CharField(min_length=5,max_length=50,required=True,widget=forms.TextInput(attrs={'placeholder':'Confirm Password'}))

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50,required=True,widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password =  forms.CharField(min_length=5,max_length=50,required=True,widget=forms.TextInput(attrs={'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ["username", "password1"]