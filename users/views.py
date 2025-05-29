from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import UserUpdateForm, PasswordChangeForm
from .models import UserProfile

@login_required
def profile_view(request):
    """
    Display the profile page for the logged-in user.
    Retrieves or creates a UserProfile instance linked to the user.
    """
    user = request.user
    try:
        profile, _ = UserProfile.objects.get_or_create(user=user)
    except Exception as e:
        messages.error(request, f"Error loading profile: {str(e)}")
        profile = None

    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_update(request):
    """
    Allow the logged-in user to update their profile information.
    Displays and processes the UserUpdateForm.
    """
    user = request.user

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        if user_form.is_valid():
            try:
                user_form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('users:profile')
            except Exception as e:
                messages.error(request, f"Error updating profile: {str(e)}")
    else:
        user_form = UserUpdateForm(instance=user)

    context = {
        'user_form': user_form,
    }
    return render(request, 'users/profile_update.html', context)
