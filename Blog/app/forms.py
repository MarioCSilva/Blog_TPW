
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


class PostCreationForm(forms.Form):
    title = forms.CharField(max_length=70,widget=forms.TextInput(attrs={"placeholder":"Title"}))
    image = forms.ImageField(allow_empty_file=True,required=False)
    text = forms.CharField(max_length=500,widget=forms.Textarea(attrs={"placeholder":"Write your message..."}))
    #page = forms.TypedChoiceField()


class BlogCreationForm(forms.Form):
    name = forms.CharField(max_length=70,widget=forms.TextInput(attrs={"placeholder":"Name"}))
    isPublic = forms.ChoiceField(choices=[("1","Public"),("2","Private")])
    data = tuple([("",x["name"]) for x in Topic.objects.all().values("name")])
    topic = forms.TypedMultipleChoiceField(choices=data)
    description = forms.CharField(max_length=500,widget=forms.TextInput(attrs={"placeholder":"Description"}))
    image = forms.ImageField(allow_empty_file=True,required=False)


class EditProfileForm(forms.Form):
    name = forms.CharField(max_length=70,required=False)
    description = forms.CharField(widget=forms.Textarea,max_length=300,required=False)
    profile_pic = forms.ImageField(allow_empty_file=True,required=False)
    birthdate = forms.DateField(required=False)
    sex = forms.ChoiceField(choices=[("Male","Male"),("Female","Female"),("Other","Other")],required=False)


