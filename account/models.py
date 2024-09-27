from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    img = models.ImageField(upload_to='account/static/', blank=True)


    rank = models.IntegerField(default=100)
    number_of_content = models.IntegerField(default=0)


    def __str__(self):
        return {
            'user': self.user,
            'phone': self.phone,
            'rank': self.rank,
            'number_of_content': self.number_of_content
        }