from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE,unique=True,related_name="profile")
    credibility = models.IntegerField()
    provider = models.CharField(max_length=20)
    avatar = models.FileField(blank=True)
    bio = models.CharField(max_length=500,blank=True)
    


class Task(models.Model):
    requester = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="requests")
    workers = models.ManyToManyField(Profile,related_name="tasks")
    title = models.CharField(max_length=100,blank="False")
    budget = models.IntegerField(blank="False")
    description = models.CharField(max_length=2000,blank="False")
    image = models.FileField(blank="True")
    date = models.DateField(auto_now_add=True)

class Work(models.Model):
    author = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="works")
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name="works")
    image = models.FileField(blank="True")
    description = models.CharField(blank="True",max_length=3000)
    date = models.DateField(auto_now_add=True)
    # dataURL = models.CharField(max_length=4000)
    # title = models.CharField(max_length=200)
    

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="post")
    time = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1024,default='')

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name="author")
    text = models.CharField(max_length=1024,default='')
    time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name="comment")