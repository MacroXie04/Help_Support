from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):

    class PostCategory(models.TextChoices):
        HELP = 'H', 'Help'
        SUPPORT = 'S', 'Support'

    class PostType(models.TextChoices):
        SINGLE = 'S', 'Single'
        MULTIPLE = 'M', 'Multiple'

    class PostStatus(models.TextChoices):
        OPEN = 'O', 'Open'
        LOCKED = 'L', 'Locked'
        EXPIRED = 'E', 'Expired'
        COMPLETED = 'C', 'Completed'



class PostApplication(models.Model):

    # Post model to represent job postings
    class ApplicationStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        APPROVED = 'A', 'Approved'
        REJECTED = 'R', 'Rejected'

    # Foreign key to the Post model
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='applications')

    # Foreign key to the applicant User model
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    # Status of the application
    status = models.CharField(max_length=10, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING)

    # Message from the applicant
    message = models.TextField(blank=True)

    # Timestamp for when the application was created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure that each applicant can only apply once to a specific post
        unique_together = ('post', 'applicant')

    def __str__(self):
        return f"Application by {self.applicant.username} for {self.post.title} - Status: {self.get_status_display()}"
