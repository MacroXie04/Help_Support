from django.db import models
from django.contrib.auth.models import User

class Content(models.Model):
    # link to user model
    publish_user = models.OneToOneField(User, on_delete=models.CASCADE)

    # state
    STATE = (
        ('W', 'Waiting to Accept'),
        ('L', 'Locked'),
        ('C', 'Completed'),

        ('R', 'Rejected due to Report'),
    )
    state = models.CharField(max_length=1, choices=STATE, default='W')

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

    # user accept
    waitlist = models.ManyToManyField(User, related_name="waitlist")

    def get_content_type_display(self):
        return dict(self.CONTENT_TYPE)[self.content_type]

    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()})"


class ReportForm(models.Model):
    # link to content model
    content = models.OneToOneField(Content, on_delete=models.CASCADE)

    # report user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # report reason
    REASON = (
        ('Racism', 'Racism'),
        ('Homosexuality Discrimination', 'Homosexuality Discrimination'),
        ('Political Discrimination', 'Political Discrimination'),
        ('Meaningless content', 'Meaningless content'),
        ('Legal risks', 'Legal risks'),
        ('Other', 'Other'),
    )
    reason = models.CharField(max_length=50, choices=REASON)

    # report message
    message = models.TextField()

    # time
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message}"
