from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os
import uuid


class UserProfile(models.Model):
    # link to user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # is active
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    # base info
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    # contact info
    phone = models.CharField(max_length=20)

    # profile info
    creatAt = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=100, blank=True)

    rank = models.IntegerField(default=100)
    number_of_content = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}"



class AccountBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user},{self.balance}"

