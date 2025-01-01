from django.db import models
from django.contrib.auth.models import User

class Content(models.Model):
    # link to user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # state
    STATE = (
        ('W', 'Waiting'),
        ('C', 'Completed'),
    )
    state = models.CharField(max_length=1, choices=STATE)

    # content type
    CONTENT_TYPE = (
        ('H', 'Help'),
        ('S', 'Support'),
    )
    content_type = models.CharField(max_length=1, choices=CONTENT_TYPE)

    # report info
    is_report = models.BooleanField(default=False)
    is_show = models.BooleanField(default=True)

    # content info
    title = models.CharField(max_length=100)
    body = models.TextField()

    # time range
    accept_time_limit = models.DateTimeField()

    created = models.DateTimeField(auto_now_add=True)

    def get_content_type_display(self):
        return dict(self.CONTENT_TYPE)[self.content_type]

    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()})"

