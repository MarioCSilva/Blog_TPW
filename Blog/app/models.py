from django.contrib.auth.models import User
from django.db import models
import os

# Create your models here.



# fazer com q o email seja unico sem necessitar de criar um abstract user.
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False


def post_pic_path(instance, filename):
    path = "post/"
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % ('img', instance.pk, ext)
    return os.path.join(path+filename)


def profile_pic_path(instance, filename):
    path = "profile/"
    return os.path.join(path+str(instance.user.id)+"."+filename.split(".")[-1])


def blog_pic_path(instance, filename):
    path = "blog/"
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % ('img', instance.pk, ext)
    return os.path.join(path+filename)


class Client(models.Model):
    name = models.CharField(max_length=50, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=True)
    profile_pic = models.ImageField(null=True,upload_to=profile_pic_path,default="default/default_profile.jpg", height_field=None, width_field=None, max_length=None)
    birthdate = models.DateField(null=True,auto_now=False, auto_now_add=False)
    sex = models.CharField(null=True, max_length=40)

    def __str__(self):
        return self.user.username


class Topic(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Blog(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ManyToManyField(Client, related_name='owner')
    subs = models.ManyToManyField(Client, related_name='subs')
    blog_pic = models.ImageField(null=True,upload_to=blog_pic_path, height_field=None, width_field=None, max_length=None)
    isPublic = models.BooleanField()
    invites = models.ManyToManyField(Client, related_name='invites', default = [])
    description = models.CharField(max_length=500, default = "")
    topic = models.ManyToManyField(Topic)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True,upload_to=post_pic_path, height_field=None, width_field=None, max_length=None)
    text = models.CharField(max_length=500)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Client, related_name='post_likes')

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=500)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
