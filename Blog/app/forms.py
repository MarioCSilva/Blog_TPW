
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


class PostCreationForm(forms.ModelForm):

    title = forms.CharField(max_length=70,widget=forms.TextInput(attrs={"placeholder":"Title"}))
    # N sei se isto da para meter ficheiros vazios ou se deixa n passar ficheiros
    image = forms.ImageField(allow_empty_file=True)
    text = forms.CharField(max_length=500,widget=forms.Textarea(attrs={"placeholder":"Write your message..."}))
    # Temos de ver isto
    page = forms.TypedChoiceField()





