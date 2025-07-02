from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# --------------------------------------------------------------------------- #
# Post (job / help request)
# --------------------------------------------------------------------------- #
class Post(models.Model):
    # --------------------------------------------------------------------- #
    # Enumerations
    # --------------------------------------------------------------------- #
    class PostCategory(models.TextChoices):
        HELP = 'H', 'Help'
        SUPPORT = 'S', 'Support'

    class PostStatus(models.TextChoices):
        OPEN = 'O', 'Open'          # accepting applications
        LOCKED = 'L', 'Locked'      # no longer accepting (full)
        EXPIRED = 'E', 'Expired'    # past deadline
        COMPLETED = 'C', 'Completed'

    # --------------------------------------------------------------------- #
    # Core fields
    # --------------------------------------------------------------------- #
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()

    category = models.CharField(
        max_length=1,
        choices=PostCategory.choices,
        default=PostCategory.HELP,
    )
    status = models.CharField(
        max_length=1,
        choices=PostStatus.choices,
        default=PostStatus.OPEN,
    )

    # Maximum number of applicants that can be **approved** for this post.
    # Set to 1 for a single-person task; >1 to allow multiple helpers.
    max_accepted_applicants = models.PositiveIntegerField(default=1)

    # Optional deadline – business logic elsewhere can set status to EXPIRED
    deadline = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --------------------------------------------------------------------- #
    # Helper methods
    # --------------------------------------------------------------------- #
    def accepted_applicants_count(self) -> int:
        """Return the number of APPROVED applications for this post."""
        return self.applications.filter(
            status=PostApplication.ApplicationStatus.APPROVED
        ).count()

    def is_full(self) -> bool:
        """Return True if the post has reached `max_accepted_applicants`."""
        return self.accepted_applicants_count() >= self.max_accepted_applicants

    def __str__(self) -> str:  # noqa: D401
        return self.title


# --------------------------------------------------------------------------- #
# PostApplication (a user's application to a Post)
# --------------------------------------------------------------------------- #
class PostApplication(models.Model):
    # --------------------------------------------------------------------- #
    # Enumerations
    # --------------------------------------------------------------------- #
    class ApplicationStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        APPROVED = 'A', 'Approved'
        REJECTED = 'R', 'Rejected'

    # --------------------------------------------------------------------- #
    # Core fields
    # --------------------------------------------------------------------- #
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='applications'
    )
    applicant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='applications'
    )

    status = models.CharField(
        max_length=1,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING,
    )
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # --------------------------------------------------------------------- #
    # Validation & persistence hooks
    # --------------------------------------------------------------------- #
    def clean(self):
        """
        Ensure an application cannot be approved if the related Post
        is already full.
        """
        if (
            self.status == self.ApplicationStatus.APPROVED
            and self.post.is_full()
            # `self` may already be in the accepted set, so exclude itself
            and not (
                self.pk
                and self.post.applications.filter(
                    pk=self.pk,
                    status=self.ApplicationStatus.APPROVED,
                ).exists()
            )
        ):
            raise ValidationError(
                "This post has already reached its maximum number of "
                "accepted applicants."
            )

    def save(self, *args, **kwargs):
        """Override save to auto-lock the Post when it becomes full."""
        # Determine if we transitioned into APPROVED status
        is_new_object = self.pk is None
        old_status = None
        if not is_new_object:
            old_status = (
                PostApplication.objects.filter(pk=self.pk)
                .values_list('status', flat=True)
                .first()
            )

        super().save(*args, **kwargs)  # perform actual save (+ clean())

        # If this application was newly approved, check whether the post filled up
        if (
            (is_new_object and self.status == self.ApplicationStatus.APPROVED)
            or (
                old_status != self.ApplicationStatus.APPROVED
                and self.status == self.ApplicationStatus.APPROVED
            )
        ):
            if self.post.is_full():
                self.post.status = Post.PostStatus.LOCKED
                self.post.save(update_fields=['status'])

    # --------------------------------------------------------------------- #
    # Meta & display
    # --------------------------------------------------------------------- #
    class Meta:
        unique_together = ('post', 'applicant')  # one application per user/post
        ordering = ('-created_at',)

    def __str__(self) -> str:  # noqa: D401
        return f"Application by {self.applicant.username} – {self.get_status_display()}"
