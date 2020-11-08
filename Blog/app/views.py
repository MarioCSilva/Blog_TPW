from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from app.forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django import forms

# Create your views here.

def main_page(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request, "main_page.html")


def entry_page(request):
    if request.method=="POST":
        if "email" in request.POST:
            print("Inside Register")
            form = RegisterForm(data=request.POST)
            if form.is_valid():
                return HttpResponse("<h1>register valid</h1>")
            else:
                return HttpResponse("<h1>register invalid</h1>")
        elif "username" in request.POST:
            form = LoginForm(data=request.POST)
            print("Inside Login")
            if form.is_valid():
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return HttpResponseRedirect('profile')
            print(form.errors)
        else:
            print("NOTHING")
            return HttpResponse("<h1>nothing</h1>")

    return render(request,"entry_page.html",{"form_login":LoginForm(),"form_register":RegisterForm()})


def profile_page(request):
    #if not request.user.is_authenticated:
     #   return redirect('/login')
    print("profile page")
    return render(request,"profile_page.html")