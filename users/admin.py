from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the UserProfile model.
    - Displays the associated user.
    - Enables search by username and email of the related user.
    """
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')
