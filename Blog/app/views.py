from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from app.forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from app.models import Client, Post, Blog, Topic
from django.db.models.functions import Length
from django.db.models import Count
from django.contrib import messages


# Create your views here.

def main_page(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == "POST":
        if "Create Post" in request.POST:
            form = PostCreationForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                text = form.cleaned_data.get('text')
                user = request.user
                client = Client.objects.get(user=user)
                topic = Topic.objects.get(name="Personal")
                blog = Blog.objects.get(topic=topic, owner__in=[client])
                post = Post(title=title, text=text, client=client, blog=blog)
                image = form.cleaned_data.get("image")
                if image:
                    post.image = image
                post.save()

                return redirect('home')
            request.session['message'] = form.errors
            return redirect('home')
        elif "Create Blog" in request.POST:
            form = BlogCreationForm(data=request.POST)
            if form.is_valid():
                name = form.cleaned_data["name"]
                topic = form.cleaned_data["topic"]
                description = form.cleaned_data["description"]
                is_public = True if form.cleaned_data.get('isPublic') == "1" else False
                client = Client.objects.get(user=request.user)
                blog = Blog(name=name, isPublic=is_public, description=description)
                blog.save()
                blog.owner.set([client])
                blog.subs.set([client])
                topics = Topic.objects.filter(id__in=topic)
                blog.topic.set(topics)
                blog.save()
                return redirect('/blog/' + str(blog.id))
            request.session['message'] = form.errors
            return redirect('home')
        else:
            return HttpResponse("<h1>nothing</h1>")
    else:
        comments = Comment.objects.all()
        post_com = {}
        for comment in comments:
            com_list = post_com.get(comment.post.id, [])
            com_list.append(comment)
            post_com[comment.post.id] = com_list

        client = Client.objects.get(user=request.user)
        post_blogs = Blog.objects.filter(isPublic=True) | Blog.objects.filter(subs__in=[client])
        # recent ones first
        posts = Post.objects.filter(blog__in=post_blogs).order_by("-date")
        # orders posts with more subs first
        blogs = Blog.objects.all().order_by(Length("subs").desc())
        print(request.GET)
        if "search_post_type" in request.GET:
            search = request.GET.get("search_post")
            choice = request.GET.get("order_choice_post")
            order = request.GET.get("order_by_post")
            # searchs for posts by name or by client name
            posts = (Post.objects.filter(title__contains=search, blog__in=post_blogs) \
                     | Post.objects.filter(client__user__username__contains=search, blog__in=post_blogs))

            if order == "asc":
                order = ""
            elif order == "desc":
                order = "-"

            if choice == "recent":
                posts = posts.order_by(order + "date")
            elif choice == "likes":
                posts = posts.order_by(order + "likes", "-date")
            elif choice == "comments":
                posts = posts.annotate(count=Count("comment")).order_by(order + "count")


        if "search_blog_type" in request.GET:
            search = request.GET.get("search_blog")
            topics = request.GET.getlist("topic_choice_blog")
            choice = request.GET.get("order_choice_blog")
            order = request.GET.get("order_by_blog")

            # searches for pages with that name or owner name
            blogs = (Blog.objects.filter(name__contains=search).distinct())  # | Blog.objects.filter(owner__user__name__in=search))
            if topics:
                blogs = blogs & (Blog.objects.filter(topic__id__in=topics).distinct())

            if order == "asc":
                order = ""
            elif order == "desc":
                order = "-"

            if choice == "subs":
                blogs = blogs.annotate(count=Count("subs")).order_by(order + "count")
            elif choice == "posts":
                blogs = blogs.annotate(count=Count("post")).order_by(order + "count")

            # blogs = blogs.order_by(Length("subs").desc())

        posts_more_det = []
        for post in posts:
            posts_detail = {}
            posts_detail["comments"] = post_com.get(post.id, [])
            posts_detail["post"] = post
            if post.likes.count() > 0:
                if client in post.likes.all():
                    posts_detail["like"] = True
                else:
                    posts_detail["like"] = False
            else:
                posts_detail["like"] = False

            topic = Topic.objects.get(name="Personal")
            blog = Blog.objects.get(owner__in=[post.client], topic=topic.id)
            posts_detail["personal"] = blog.id

            posts_more_det.append(posts_detail)
        if "search_query" in request.GET:
            search_query = "blog"
            print("pls")
        else:
            search_query = "post"
        return render(request, "main_page.html",
                      {"form_post": PostCreationForm(), "form_blog": BlogCreationForm(),
                       "blogs": blogs,
                       "posts_more_det": posts_more_det,
                       "search_post_form": FilterPostForm(),
                       "search_blog_form": FilterBlogForm(),
                       "search_query": search_query})


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
                return redirect('/my_profile')
            else:
                print(form.errors)
                return render(request, "entry_page.html",
                              {"form_login": LoginForm(), "form_register": RegisterForm(), "form_errors": form.errors})

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


def profile_page(request, name):
    if not request.user.is_authenticated or request.method not in ["GET", "POST"]:
        return redirect('/login')

    user = Client.objects.get(user__username=name)
    owner = request.user.username == name

    if request.method == "GET":
        return render(request, "profile_page.html",
                      {"client": user, "form_edit": EditProfileForm(instance=user), "owner": owner})
    elif request.method == "POST":

        form = EditProfileForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            print("valid")
            client = form.save(commit=False)
            client.save()
            return redirect("/profile/" + name)
        print("not valid")
        return render(request, "profile_page.html", {"client": user, "form_edit": form, "form_errors": form.errors})


def my_profile(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return redirect("/profile/" + str(request.user.username))


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

    if "search_post" in request.GET:

        search = request.GET.get("search_post")
        choice = request.GET.get("order_choice_post")
        order = request.GET.get("order_by_post")
        # searchs for posts by name or by client name
        posts = (Post.objects.filter(title__contains=search, blog=blog.id) \
                 | Post.objects.filter(client__user__username__contains=search, blog=blog.id))

        if order == "asc":
            order = ""
        elif order == "desc":
            order = "-"

        if choice == "recent":
            posts = posts.order_by(order + "date")
        elif choice == "likes":
            posts = posts.order_by(order + "likes", "-date")
        elif choice == "comments":
            posts = posts.annotate(count=Count("comment")).order_by(order + "count")

    comments = Comment.objects.all()
    post_com = {}
    for comment in comments:
        com_list = post_com.get(comment.post.id, [])
        com_list.append(comment)
        post_com[comment.post.id] = com_list

    posts_more_det = []
    for post in posts:
        posts_detail = {}
        posts_detail["comments"] = post_com.get(post.id, [])
        posts_detail["post"] = post
        if post.likes.count() > 0:
            if client in post.likes.all():
                posts_detail["like"] = True
            else:
                posts_detail["like"] = False
        else:
            posts_detail["like"] = False

        topic = Topic.objects.get(name="Personal")
        blog_personal = Blog.objects.get(owner__in=[client], topic=topic.id)
        posts_detail["personal"] = blog_personal.id
        posts_more_det.append(posts_detail)
    return render(request, "blog_page.html", {
        "blog": blog,
        "permission": permission,
        "personal": personal,
        "subbed": subbed,
        "posts_more_det": posts_more_det,
        "blog_owners": EditBlogOwners(),
        "blog_topics": EditBlogTopics(blog_topics=blog.topic),
        "blog_subs": EditBlogSubs(blog_id=blog.id, blog_user=request.user.username),
        "blog_edit": EditBlog(blog_name=blog.name, blog_description=blog.description),
        "blog_invites": EditBlogInvites(blog_id=blog.id),
        "blog_post": PostCreationForm(),
        "blog_pic_form": EditBlogPic(),
        "search_post_form": FilterPostForm()
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
    blog_id = request.GET.get('blog_id')
    if form.is_valid():
        username = form.cleaned_data.get('username')
        if len(User.objects.filter(username=username)) == 0 or username == request.user.username:
            messages.error(request, "User does not exist.")
            return redirect('/blog/' + blog_id)
        cli_user = User.objects.get(username=username)
        client = Client.objects.get(user=cli_user)
        blog = Blog.objects.get(id=blog_id)
        blog.owner.add(client)
        blog.save()
        return redirect('/blog/' + blog_id)
    else:
        messages.error(request, form.errors)
        return redirect('/blog/' + blog_id)


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
        messages.error(request, form.errors)
        return redirect('/blog/' + blog_id)


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
        messages.error(request, form.errors)
        return redirect('/blog/' + blog_id)


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
        messages.error(request, form.errors)
        return redirect('/blog/' + blog_id)


def blog_follow(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    blog_id = request.GET.get('blog_id')
    blog = Blog.objects.get(id=blog_id)
    option = request.GET.get('Option')
    client = Client.objects.get(user=request.user)

    if option == "Follow":
        if blog.isPublic:
            messages.success(request, 'Successfully followed this blog.')
            blog.subs.add(client)
        else:
            messages.warning(request, 'Request sent to follow this blog.')
            blog.invites.add(client)
    elif option == "Unfollow":
        messages.success(request, 'Successfully unfollowed this blog.')
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
        messages.error(request, form.errors)
        return redirect('/blog/' + blog_id)


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
        client = Client.objects.get(user=user)
        post = Post(title=title, text=text, client=client, blog=blog)
        image = form.cleaned_data.get("image")
        if image:
            post.image = image
        post.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.error(request, form.errors)
        return redirect('/blog/' + blog_id)


def settings(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if request.method == "GET":
        security = RegisterForm()

        return render(request, "settings.html", {"form_security": RegisterForm(instance=request.user)})
    elif request.method == "POST":
        print(request.POST)
        if "security" in request.POST:
            user = User.objects.get(id=request.user.id)
            form = RegisterForm(request.POST, instance=user)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return render(request, "settings.html", {"form_security": RegisterForm(instance=user), "valid": True})
            print(form.errors)
            return render(request, "settings.html",
                          {"form_security": RegisterForm(data=request.POST), "form_security_errors": form.errors})

        if "delete" in request.POST:
            try:
                user = User.objects.get(id=request.user.id)
                # logout(request.user)
                user.delete()
            except User.DoesNotExist:
                return render(request, "settings.html", {"errors": "User does not exist"})
            except Exception as e:
                return render(request, "settings.html", {"errors": e.message})
            return redirect("/login")


def post_comment(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    text = request.GET.get('com_text')
    client = Client.objects.get(user=request.user)

    comment = Comment(text=text, client=client, post=post)
    comment.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


def post_like(request):
    if request.is_ajax():
        if not request.user.is_authenticated:
            return redirect('/login')
        try:
            username = request.GET['username']
            post_id = request.GET.get('post_id')
            post = Post.objects.get(id=post_id)
            like = request.GET.get('like')
            client = Client.objects.get(user=request.user)
            if like == "like":
                post.likes.add(client)
            else:
                post.likes.remove(client)

            post.save()

            return HttpResponse('Liked post!')
            # perform operations on the user name.
        except:
            return HttpResponse('Something went wrong!')
        return HttpResponse('sucess')
    else:
        return HttpResponse('sucess')


def blog_pic(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    blog_id = request.POST.get('blog_id')
    blog = Blog.objects.get(id=blog_id)
    form = EditBlogPic(data=request.POST, files=request.FILES)
    if form.is_valid():
        print(form.cleaned_data["blog_pic"])
        blog.blog_pic = form.cleaned_data["blog_pic"]
        blog.save()
        return redirect('/blog/' + blog_id)
    else:
        messages.error(request, form.errors)
        return redirect('/blog/' + blog_id)
