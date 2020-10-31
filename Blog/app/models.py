from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.username


class Followers(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return self.follower + "," + self.following


class Page(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ManyToManyField(User, related_name='owner')
    subs = models.ManyToManyField(User, related_name='subs')
    visibility = models.ManyToManyField(User, related_name='visibility')
    isPublic = models.BooleanField()
    invites = models.ManyToManyField(User, related_name='invites')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    #image = models.ImageField()
    text = models.CharField(max_length=500)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
