from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Content(models.Model):
    content = models.TextField()
    push_user = models.ForeignKey(User, on_delete=models.CASCADE)
    push_time  = models.DateTimeField(auto_now_add=True)
    time_limit = models.DateTimeField()
    state = models.TextField(blank=True)
    accept_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_content')

    def __str__(self):
        return self.state


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user