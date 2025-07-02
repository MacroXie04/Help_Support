import uuid
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
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        help_text="Public-facing identifier for lookup"
    )
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

    # Maximum number of applicants that can be approved for this post.
    max_accepted_applicants = models.PositiveIntegerField(default=1)

    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --------------------------------------------------------------------- #
    # Helper methods
    # --------------------------------------------------------------------- #
    def accepted_applicants_count(self) -> int:
        """Return number of APPROVED applications for this post."""
        return self.applications.filter(
            status=PostApplication.ApplicationStatus.APPROVED
        ).count()

    def is_full(self) -> bool:
        """True if the post has reached its applicant limit."""
        return self.accepted_applicants_count() >= self.max_accepted_applicants

    def __str__(self) -> str:  # noqa: D401
        return f'{self.title}, {self.get_category_display()} Post by {self.author.username}'


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
        Prevent approving an application if the related Post is already full.
        """
        if (
            self.status == self.ApplicationStatus.APPROVED
            and self.post.is_full()
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
        """Override save to auto-lock Post when it becomes full."""
        is_new = self.pk is None
        old_status = None
        if not is_new:
            old_status = (
                PostApplication.objects.filter(pk=self.pk)
                .values_list('status', flat=True)
                .first()
            )

        super().save(*args, **kwargs)  # performs clean()

        transitioned_to_approved = (
            (is_new and self.status == self.ApplicationStatus.APPROVED)
            or (
                old_status != self.ApplicationStatus.APPROVED
                and self.status == self.ApplicationStatus.APPROVED
            )
        )
        if transitioned_to_approved and self.post.is_full():
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
