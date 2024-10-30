from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from index.models import HelpContent
from django.utils import timezone


class UserActivate(models.Model):
    # last login time
    last_login = models.DateTimeField(auto_now=False)
    last_fetch_time = models.DateTimeField(auto_now=False)

    # user info
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return {
            'user': self.user,
            'last_fetch_time': self.last_fetch_time,
        }


class HelpChat(models.Model):
    # unique foreign key link to HelpContent
    chat = models.OneToOneField(HelpContent, on_delete=models.CASCADE)


class HelpMessage(models.Model):
    chat = models.OneToOneField(HelpContent, on_delete=models.CASCADE)
    message = models.TextField()
    message_time = models.DateTimeField(default=timezone.now)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.message
