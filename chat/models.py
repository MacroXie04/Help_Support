from django.db import models
from django.contrib.auth.models import User
from postings.models import Post


class ChatRoom(models.Model):
    """One‑to‑one mapping with Post; participants auto‑synced."""
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="chat_room")
    participants = models.ManyToManyField(User, related_name="chat_rooms", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def sync_participants(self):
        """Ensure author + approved applicants are in the room."""
        approved_users = User.objects.filter(
            applications__post=self.post,
            applications__status='A',  # APPROVED
        )
        self.participants.set([self.post.author, *approved_users])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Always (re‑)sync after save
        self.sync_participants()

    def __str__(self):
        return f"Chat for {self.post.title} ({self.post.uuid})"


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:30]}…"