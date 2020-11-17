from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from app.forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from app.models import Client,Followers,Post,Blog, Topic

# Create your views here.

def main_page(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == "POST":
        if "Create Post" in request.POST:
            form = PostCreationForm(data=request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                text = form.cleaned_data.get('text')
                user = request.user
                image = form.cleaned_data.get("image")
                client = Client.objects.get(user=user)
                topic = Topic.objects.get(name="Personal")
                blog = Blog.objects.get(topic = topic, owner__in = [client])
                post = Post(title = title, text = text, client = client, blog = blog, image=image)
                post.save()

                return redirect('home')
        elif "Create Blog" in request.POST:
            form = BlogCreationForm(data=request.POST)
            if form.is_valid():
                name = form.cleaned_data["name"]
                topic = form.cleaned_data.get('topic')
                isPublic = True if form.cleaned_data.get('isPublic') == "Public" else False
                client = Client.objects.get(user=request.user)
                blog = Blog(name=name, isPublic=isPublic)
                blog.save()
                blog.owner.set([client])
                blog.subs.set([client])
                topics = Topic.objects.filter(name__in=topic)
                blog.topic.set(topics)

                return redirect('home')
        else:        
            return HttpResponse("<h1>nothing</h1>")
    else:
        client = Client.objects.get(user=request.user)
        
        post_blogs = Blog.objects.filter(isPublic=True) | Blog.objects.filter(subs__in = [client])
        posts = Post.objects.filter(blog__in = post_blogs)
        
        blogs = Blog.objects.all()
 
        return render(request, "main_page.html",{"form_post":PostCreationForm(),"form_blog":BlogCreationForm(),"posts":posts, "blogs":blogs})


def entry_page(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method=="POST":
        if "email" in request.POST:
            form = RegisterForm(data=request.POST)
            if form.is_valid():
                user=form.save()
                user.refresh_from_db()                
                user.save()
                client = Client(user=user)
                client.save()
                name = user.username
                topic = Topic.objects.get(name="Personal")
                isPublic = True
                blog = Blog(name=name, isPublic=isPublic)
                blog.save()
                blog.owner.set([client])
                blog.subs.set([client])
                blog.topic.set([topic])
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
            return HttpResponse("<h1>nothing</h1>")
        
    elif request.method == "GET":
        return render(request,"entry_page.html",{"form_login":LoginForm(),"form_register":RegisterForm()})


def profile_page(request):

    if not request.user.is_authenticated:
        return redirect('/login')
    user = Client.objects.get(user=request.user.id)
    return render(request,"profile_page.html",{"user":user})

