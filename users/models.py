from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """
    Extends the built-in User model with additional profile information.
    Currently, this model serves as a placeholder for user-related profile data.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    email_notifications = models.BooleanField(default=True)
    task_reminders = models.BooleanField(default=True)
    daily_digest = models.BooleanField(default=False)
    theme_preference = models.CharField(
        max_length=10,
        choices=[
            ("light", "Light"),
            ("dark", "Dark"),
            ("auto", "Auto"),
        ],
        default="light",
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
