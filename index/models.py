from django.db import models

# Create your models here.

class Content(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    generate_time  = models.DateTimeField(auto_now_add=True)
    push_user = models.CharField(max_length=100)


    def __str__(self):
        return self.title

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    register_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username