from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from django.contrib import messages
from django.shortcuts import redirect

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter for handling social authentication.
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Handle social login before the account is connected.
        """
        # If user is already logged in, connect the social account
        if request.user.is_authenticated:
            return
        
        # Check if email already exists in the system
        if sociallogin.account.extra_data.get('email'):
            email = sociallogin.account.extra_data['email']
            from django.contrib.auth.models import User
            
            try:
                existing_user = User.objects.get(email=email)
                # Connect this social account to existing user
                sociallogin.connect(request, existing_user)
                messages.success(
                    request, 
                    f'Successfully connected your {sociallogin.account.provider} account!'
                )
            except User.DoesNotExist:
                pass
    
    def save_user(self, request, sociallogin, form=None):
        """
        Save user information from social login.
        """
        user = super().save_user(request, sociallogin, form)
        
        # Extract additional information from social account
        extra_data = sociallogin.account.extra_data
        
        if not user.first_name and 'first_name' in extra_data:
            user.first_name = extra_data['first_name']
        
        if not user.last_name and 'last_name' in extra_data:
            user.last_name = extra_data['last_name']
        
        user.save()
        
        # Create welcome message
        messages.success(
            request,
            f'Welcome! Your account has been created using {sociallogin.account.provider.title()}.'
        )
        
        return user