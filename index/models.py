from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Content(models.Model):
    content = models.TextField()
    push_type = models.CharField(max_length=100)
    state = models.TextField(blank=True)

    push_time  = models.DateTimeField(auto_now_add=True)
    time_limit = models.IntegerField(default=0, blank=True)

    accept_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_content')
    push_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.state
