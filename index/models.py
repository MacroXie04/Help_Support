from django.db import models
from django.contrib.auth.models import User


class HelpContent(models.Model):
    # content and enhanced content in HTML format
    content = models.TextField()
    enhanced_content = models.TextField(blank=True)

    # time info
    creat_time = models.DateTimeField(auto_now_add=True)
    time_limit = models.DateTimeField(blank=True)

    # state info
    is_show = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    completed_data = models.DateTimeField(blank=True)
    state = models.TextField(default='waiting for accept')

    # money info
    total_money = models.FloatField(default=0.0)
    money_per_user = models.FloatField(default=0.0)

    # foreign key link to push and accept users
    max_accept_user = models.IntegerField(default=1)
    push_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='helpcontent_push_users')
    unverified_accept_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                               related_name='helpcontent_unverified_users')
    verified_accept_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='helpcontent_verified_users')

    def __str__(self):
        return self.state


class SupportContent(models.Model):
    # content and enhanced content in HTML format
    content = models.TextField()
    enhanced_content = models.TextField(blank=True)

    # time info
    creat_time = models.DateTimeField(auto_now_add=True)
    time_limit = models.DateTimeField(blank=True)

    # state info
    is_show = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    state = models.TextField(default='waiting for accept')

    # foreign key link to push and accept users
    max_accept_user = models.IntegerField(default=1)
    push_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supportcontent_push_users')
    unverified_accept_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                               related_name='supportcontent_unverified_users')
    verified_accept_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                             related_name='supportcontent_verified_users')

    def __str__(self):
        return self.state
