from django.contrib.auth.models import User
from django.db import models
import os

# Create your models here.


########### METER PASSES OCULTAS, E MOSTRAR MENSAGENS DE ERROS DEPOIS e sessions


def profile_pic_path(instance, filename):
    path = "profile/"
    return os.path.join(path+instance.user.username+"."+filename.split(".")[-1])

def post_pic_path(instance, filename):
    path = "post/"
    return os.path.join(path+instance._id+"."+filename.split(".")[-1])

def blog_pic_path(instance, filename):
    path = "blog/"
    return os.path.join(path+instance._id+"."+filename.split(".")[-1])


class Client(models.Model):
    name = models.CharField(max_length=50, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=True)
    profile_pic = models.ImageField(null=True,upload_to=profile_pic_path, height_field=None, width_field=None, max_length=None)
    birthdate = models.DateField(null=True,auto_now=False, auto_now_add=False)
    sex = models.CharField(null=True, max_length=40)

    def __str__(self):
        return self.user.username


# class Followers(models.Model):
#     follower = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='follower')
#     following = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='following')

#     def __str__(self):
#         return self.follower + "," + self.following


class Topic(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Blog(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ManyToManyField(Client, related_name='owner')
    subs = models.ManyToManyField(Client, related_name='subs')
    blog_pic = models.ImageField(null=True,upload_to=blog_pic_path, height_field=None, width_field=None, max_length=None)
    #visibility = models.ManyToManyField(Client, related_name='visibility')
    isPublic = models.BooleanField()
    invites = models.ManyToManyField(Client, related_name='invites', default = [])
    description = models.CharField(max_length=500, default = "")
    topic = models.ManyToManyField(Topic)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True,upload_to=post_pic_path, height_field=None, width_field=None, max_length=None)
    text = models.CharField(max_length=500)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

