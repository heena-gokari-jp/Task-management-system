from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import UserUpdateForm, PasswordChangeForm
from .models import UserProfile

@login_required
def profile_view(request):
    user = request.user
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_update(request):
    user = request.user
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=user)
    
    context = {
        'user_form': user_form,
    }
    return render(request, 'users/profile_update.html', context)
