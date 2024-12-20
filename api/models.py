from django.db import models
from django.contrib.auth.models import User


class Content(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    average_vote = models.FloatField(default=0.0)


class Vote(models.Model):
    content = models.ForeignKey(
        Content,
        related_name="votes",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    score = models.PositiveIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["content"]),
            models.Index(fields=["user"]),
            models.Index(fields=["content", "user"]),
        ]
