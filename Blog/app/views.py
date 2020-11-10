from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from app.forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from app.models import *

# Create your views here.

def main_page(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request, "main_page.html")


def entry_page(request):
    if request.method=="POST":
        if "email" in request.POST:
            form = RegisterForm(data=request.POST)
            if form.is_valid():
                user=form.save()
                user.refresh_from_db()                
                user.save()
                client = Client(user=user)
                client.save()
                login(request, user)
                return redirect('home')
            else:
                print(form.errors)

        elif "username" in request.POST:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                if user is not None:
                    login(request, user)
                    return redirect('profile')
                #passar os dados do utilizador
            else:
                print(form.errors)

        else:        
            print("NOTHING")
            return HttpResponse("<h1>nothing</h1>")
    elif request.method == "GET":
        return render(request,"entry_page.html",{"form_login":LoginForm(),"form_register":RegisterForm()})


def profile_page(request):
    #if not request.user.is_authenticated:
     #   return redirect('/login')
    print("profile page")
    return render(request,"profile_page.html")