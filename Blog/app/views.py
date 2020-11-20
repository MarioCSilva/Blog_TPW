from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from app.forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from app.models import Client, Post, Blog, Topic
from django.db.models.functions import Length

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

        # recent ones first
        posts = Post.objects.filter(blog__in=post_blogs).order_by("-date")

        # orders posts with more subs first
        blogs = Blog.objects.all().order_by(Length("subs").desc())

        if "search_post" in request.GET:
            search = request.GET["search_post"]
            # searchs for posts by name or by client name
            posts =  Post.objects.filter(title__contains=search,blog__in=post_blogs)\
                     | Post.objects.filter(client__user__username__contains=search,blog__in=post_blogs)
            # recent ones first
            posts = posts.order_by("-date")

        if "search_blog" in request.GET:
            search = request.GET["search_blog"]
            # searches for pages with that name or owner name
            blogs = Blog.objects.filter(name__contains=search) | Blog.objects.filter(owner__user__name__in=search)
            blogs = blogs.order_by(Length("subs").desc())



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
                is_public = True
                blog = Blog(name=name, isPublic=is_public)
                blog.save()
                blog.owner.add(client.id)
                blog.subs.add(client.id)
                blog.topic.add(topic.id)
                blog.save()
                login(request, user)
                return redirect('profile')
            else:
                print(form.errors)
                return render(request, "entry_page.html", {"form_login": LoginForm(), "form_register": RegisterForm(),"form_errors":form.errors})

        elif "username" in request.POST:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                # passar os dados do utilizador
            else:
                print(form.errors)
                return render(request, "entry_page.html",
                              {"form_login": LoginForm(), "form_register": RegisterForm(), "form_errors2": form.errors})

        else:
            return render(request, "entry_page.html", {"form_login": LoginForm(), "form_register": RegisterForm()})

    elif request.method == "GET":
        return render(request, "entry_page.html", {"form_login": LoginForm(), "form_register": RegisterForm()})


def profile_page(request):
    if not request.user.is_authenticated or request.method not in ["GET","POST"]:
        return redirect('/login')
    user = Client.objects.get(user=request.user.id)

    if request.method == "GET":
        return render(request, "profile_page.html", {"client": user, "form_edit": EditProfileForm()})
    elif request.method == "POST":
        form = EditProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            client = Client.objects.get(user=request.user.id)
            name = form.cleaned_data["name"]
            if name:
                client.name = name
            birthdate = form.cleaned_data["birthdate"]
            if birthdate:
                client.birthdate = birthdate
            profile_pic = form.cleaned_data["profile_pic"]
            print(profile_pic)
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
        return render(request, "profile_page.html", {"client": user, "form_edit": EditProfileForm(),"form_errors":form.errors})

def blog_page(request, num):
    if not request.user.is_authenticated:
        return redirect('/login')
    blog = Blog.objects.get(id=num)
    client = Client.objects.get(user=request.user.id)
    personal = False
    for topic in blog.topic.all():
        if topic.name == "Personal":
            personal = True
    permission = False
    if client in blog.owner.all():
        permission = True
    subbed = False
    posts = Post.objects.filter(blog=blog.id)
    if client in blog.subs.all():
        subbed = True
    return render(request, "blog_page.html", {
        "blog": blog,
        "permission": permission,
        "personal": personal,
        "subbed": subbed,
        "posts": posts,
        "blog_owners": EditBlogOwners(),
        "blog_topics": EditBlogTopics(blog_topics=blog.topic),
        "blog_subs": EditBlogSubs(blog_id=blog.id, blog_user=request.user.username),
        "blog_edit": EditBlog(blog_name=blog.name, blog_description=blog.description),
        "blog_invites": EditBlogInvites(blog_id=blog.id),
        "blog_post": PostCreationForm(),
    })


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
    blog_id = request.GET.get('blog_id')
    blog = Blog.objects.get(id=blog_id)
    form = EditBlogTopics(data=request.GET, blog_topics=blog.topic)
    if form.is_valid():
        topics_select = form.cleaned_data.get('topics_select')
        topics_unselect = form.cleaned_data.get('topics_unselect')
        topics = topics_select + topics_unselect
        personal = Topic.objects.get(name="Personal")
        if personal in blog.topic.all():
            topics += [str(personal.id)]
        topics = Topic.objects.filter(id__in=[int(x) for x in topics])
        print(topics)
        blog.topic.set(topics)
        blog.save()
        return redirect('/blog/' + blog_id)
    else:
        print(form.errors)


def blog_subs(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    blog_id = request.GET.get('blog_id')
    form = EditBlogSubs(data=request.GET, blog_id=blog_id, blog_user=request.user.username)
    if form.is_valid():
        blog = Blog.objects.get(id=blog_id)
        subs = form.cleaned_data.get('subs')
        subs = [Client.objects.get(user=int(x)) for x in subs]
        print(subs)
        blog.subs.set(subs)
        client = Client.objects.get(user=request.user)
        blog.subs.add(client)
        blog.save()
        return redirect('/blog/' + blog_id)
    else:
        print(form.errors)


def blog_edit(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    blog_id = request.GET.get('blog_id')
    blog = Blog.objects.get(id=blog_id)
    form = EditBlog(data=request.GET, blog_name=blog.name, blog_description=blog.description)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        description = form.cleaned_data.get('description')
        blog.name = name
        blog.description = description
        blog.save()
        return redirect('/blog/' + blog_id)
    else:
        print(form.errors)


def blog_follow(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    blog_id = request.GET.get('blog_id')
    blog = Blog.objects.get(id=blog_id)
    option = request.GET.get('Option')
    client = Client.objects.get(user=request.user)

    if option == "Follow":
        if blog.isPublic:
            blog.subs.add(client)
        else:
            blog.invites.add(client)
    elif option == "Unfollow":
        blog.subs.remove(client)

    blog.save()
    return redirect('/blog/' + blog_id)


def blog_delete(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    blog_id = request.GET.get('blog_id')
    blog = Blog.objects.get(id=blog_id)

    blog.delete()
    return redirect('/')


def blog_visibility(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    blog_id = request.GET.get('blog_id')
    blog = Blog.objects.get(id=blog_id)

    is_public = request.GET.get('visibility')
    blog.isPublic = is_public
    blog.save()
    return redirect('/blog/' + blog_id)


def blog_invites(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    blog_id = request.GET.get('blog_id')
    blog = Blog.objects.get(id=blog_id)
    form = EditBlogInvites(data=request.GET, blog_id=blog_id)
    if form.is_valid():
        accepted_invites = form.cleaned_data.get('invites')
        unaccepted_invites = [x.id for x in blog.invites.all() if x.id not in [int(y) for y in accepted_invites]]
        blog.invites.set(unaccepted_invites)
        for x in accepted_invites:
            blog.subs.add(int(x))
        blog.save()
        return redirect('/blog/' + blog_id)
    else:
        print(form.errors)


def blog_post(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    blog_id = request.GET.get('blog_id')
    blog = Blog.objects.get(id=blog_id)
    form = PostCreationForm(data=request.GET)
    if form.is_valid():
        title = form.cleaned_data.get('title')
        text = form.cleaned_data.get('text')
        user = request.user
        image = form.cleaned_data.get("image")
        client = Client.objects.get(user=user)
        post = Post(title=title, text=text, client=client, blog=blog, image=image)
        post.save()
        return redirect('/blog/' + blog_id)
    else:
        print(form.errors)
