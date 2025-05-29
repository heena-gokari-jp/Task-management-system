from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Extends the built-in User model with additional profile information.
    Currently, this model serves as a placeholder for user-related profile data.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    def __str__(self):
        return f"{self.user.username}'s profile"
