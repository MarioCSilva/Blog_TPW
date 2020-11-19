from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from app.forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from app.models import Client, Post, Blog, Topic


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
                blog = Blog.objects.get(topic=topic, owner__in=[client])
                post = Post(title=title, text=text, client=client, blog=blog, image=image)
                post.save()

                return redirect('home')
        elif "Create Blog" in request.POST:
            form = BlogCreationForm(data=request.POST)
            if form.is_valid():
                name = form.cleaned_data["name"]
                topic = form.cleaned_data["topic"]
                print(topic)
                is_public = True if form.cleaned_data.get('isPublic') == "1" else False
                client = Client.objects.get(user=request.user)
                blog = Blog(name=name, isPublic=is_public)
                blog.save()
                blog.owner.set([client])
                blog.subs.set([client])
                topics = Topic.objects.filter(id__in=topic)
                blog.topic.set(topics)
                print(topics)
                blog.save()
                return redirect('home')
        else:
            return HttpResponse("<h1>nothing</h1>")
    else:
        client = Client.objects.get(user=request.user)

        post_blogs = Blog.objects.filter(isPublic=True) | Blog.objects.filter(subs__in=[client])
        posts = Post.objects.filter(blog__in=post_blogs)

        blogs = Blog.objects.all()

        return render(request, "main_page.html",
                      {"form_post": PostCreationForm(), "form_blog": BlogCreationForm(), "posts": posts,
                       "blogs": blogs})


def entry_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        if "email" in request.POST:
            form = RegisterForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                user.save()
                client = Client(user=user)
                client.save()
                name = user.username
                topic = Topic.objects.get(name="Personal")
                is_public = False
                blog = Blog(name=name, isPublic=is_public)
                blog.save()
                blog.owner.add(client.id)
                blog.subs.add(client.id)
                blog.topic.add(topic.id)
                blog.save()
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
                # passar os dados do utilizador
            else:
                print(form.errors)

        else:
            return HttpResponse("<h1>nothing</h1>")

    elif request.method == "GET":
        return render(request, "entry_page.html", {"form_login": LoginForm(), "form_register": RegisterForm()})


def profile_page(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == "GET":
        user = Client.objects.get(user=request.user.id)
        return render(request,"profile_page.html",{"client":user,"form_edit":EditProfileForm()})
    elif request.method == "POST":
        form = EditProfileForm(data=request.POST)
        if form.is_valid():
            client = Client.objects.get(user=request.user.id)
            name = form.cleaned_data["name"]
            if name:
                client.name = name
            birthdate = form.cleaned_data["birthdate"]
            if birthdate:
                client.birthdate = birthdate
            profile_pic = form.cleaned_data["profile_pic"]
            if profile_pic:
                client.profile_pic = profile_pic
            description = form.cleaned_data["description"]
            if description:
                client.description = description
            sex = form.cleaned_data["sex"]
            if sex:
                client.sex = sex
            client.save()
            return redirect("profile")



def blog_page(request, num):
    if not request.user.is_authenticated:
        return redirect('/login')
    blog = Blog.objects.get(id=num)
    client = Client.objects.get(user=request.user.id)
    if client not in blog.owner.all() and not blog.isPublic and client not in blog.subs.all():
        print(blog.isPublic)
        return redirect("home")
    permission = False
    if client in blog.owner.all():
        permission = True

    return render(request, "blog_page.html", {"blog": blog,
                                              "permission": permission,
                                              "blog_owners": EditBlogOwners(),
                                              "blog_topics": EditBlogTopics()})


def my_blog(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    client = Client.objects.get(user=request.user.id)
    topic = Topic.objects.get(name="Personal")
    blog = Blog.objects.get(owner__in=[client], topic=topic.id)
    return redirect("/blog/" + str(blog.id))


def blog_owners(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    form = EditBlogOwners(data=request.GET)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        cli_user = User.objects.get(username=username)
        blog_id = request.GET.get('blog_id')
        if cli_user is None or username == request.user.username:
            return redirect('/blog/' + blog_id)
        client = Client.objects.get(user=cli_user)
        blog = Blog.objects.get(id=blog_id)
        blog.owner.add(client)
        blog.save()
        return redirect('/blog/' + blog_id)
    else:
        print(form.errors)


def blog_topics(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    form = EditBlogTopics(data=request.GET)
    print("ww")
    if form.is_valid():
        blog_id = request.GET.get('blog_id')
        client = Client.objects.get(user=request.user)
        blog = Blog.objects.get(id=blog_id)
        topics = request.GET.get('topics')
        blog.topic.set(topics)
        blog.save()
        return redirect('/blog/' + blog_id)
    else:
        print(form.errors)
