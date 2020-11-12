from django.contrib.auth.models import User
from django.db import models

# Create your models here.


########### METER PASSES OCULTAS, E MOSTRAR MENSAGENS DE ERROS DEPOIS e sessions





class Client(models.Model):
    name = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=True)
    profile_pic = models.ImageField(null=True,upload_to="profile/", height_field=None, width_field=None, max_length=None)
    birthdate = models.DateField(null=True,auto_now=False, auto_now_add=False)
    sex = models.CharField(null=True, max_length=40)

    def __str__(self):
        return self.user.username


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
    date = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True,upload_to="posts/", height_field=None, width_field=None, max_length=None)
    text = models.CharField(max_length=500)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
