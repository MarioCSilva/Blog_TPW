from django.shortcuts import render, redirect
from app.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django import forms

# Create your views here.

def main_page(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request, "main_page.html")


def entry_page(request):
    if request.method=="POST":
        if "register" in request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
                print("valid")
                
                return redirect('profile_page')
            else:
                return redirect("profile_page")
        elif "login" in request.POST:
            form = AuthenticationForm(request.POST)
            if form.is_valid():
                #form.save()
                #username = form.cleaned_data.get('username')
                #raw_password = form.cleaned_data.get('password1')
                #user = authenticate(username=username, password=raw_password)
                #login(request, user)
                return redirect('profile_page')
            else:
                return redirect("profile_page")
        else:
            return redirect("profile_page")

    return render(request,"entry_page.html",{"form_login":AuthenticationForm(),"form_register":RegisterForm()})


def profile_page(request):
    #if not request.user.is_authenticated:
     #   return redirect('/login')
    return render(request,"profile_page.html")