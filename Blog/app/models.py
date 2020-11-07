from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    description = models.CharField(max_length=300)
    profile_pic = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    birthdate = models.DateField(auto_now=False, auto_now_add=False)
    
    def __str__(self):
        return self.username


class Followers(models.Model):
    follower = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return self.follower + "," + self.following


class Page(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ManyToManyField(Client, related_name='owner')
    subs = models.ManyToManyField(Client, related_name='subs')
    visibility = models.ManyToManyField(Client, related_name='visibility')
    isPublic = models.BooleanField()
    invites = models.ManyToManyField(Client, related_name='invites')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField()
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    text = models.CharField(max_length=500)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
