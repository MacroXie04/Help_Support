from django.db import models
from django.contrib.auth.models import User


class HelpContent(models.Model):
    # content and enhanced content in HTML format
    content = models.TextField()

    # time info
    creat_time = models.DateTimeField(auto_now_add=True)
    accept_time_limit = models.DateTimeField(blank=True, null=True)

    # state info
    is_show = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    completed_data = models.DateTimeField(blank=True, null=True)
    state = models.TextField(default='waiting for accept')

    # money info
    total_money = models.FloatField(default=0.0)

    # foreign key link to push and accept users
    max_accept_user = models.IntegerField(default=1)
    push_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='HelpContent_push_users')
    unverified_accept_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                               related_name='HelpContent_unverified_users', blank=True, null=True)
    verified_accept_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                             related_name='HelpContent_verified_users', blank=True, null=True)

    def __str__(self):
        return self.push_user.username + ' ' + self.state + ' ' + self.content


class SupportContent(models.Model):
    # content and enhanced content in HTML format
    content = models.TextField()

    # time info
    creat_time = models.DateTimeField(auto_now_add=True)
    accept_time_limit = models.DateTimeField(blank=True, null=True)

    # state info
    is_show = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    completed_data = models.DateTimeField(blank=True, null=True)
    state = models.TextField(default='waiting for accept')

    # money info
    total_money = models.FloatField(default=0.0)

    # foreign key link to push and accept users
    max_accept_user = models.IntegerField(default=1)
    push_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='SupportContent_push_users')
    unverified_accept_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                               related_name='SupportContent_unverified_users', blank=True, null=True)
    verified_accept_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                             related_name='SupportContent_verified_users', blank=True, null=True)

    def __str__(self):
        return self.push_user.username + ' ' + self.state + self.content
