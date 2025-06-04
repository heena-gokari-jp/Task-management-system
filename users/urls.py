from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    # Display user profile
    path("profile/", views.profile_view, name="profile"),
    # Update user profile form
    path("profile/update/", views.profile_update, name="profile_update"),
]
