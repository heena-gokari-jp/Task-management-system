from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserUpdateForm(forms.ModelForm):
    """
    Form for updating basic user information including username, email,
    first name, and last name.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class PasswordChangeForm(forms.Form):
    """
    Custom form for handling password change with confirmation.
    Includes validation to ensure new password and confirmation match.
    """
    current_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        """
        Validates that the new password and confirmation password match.
        """
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords don't match.")

        return cleaned_data
