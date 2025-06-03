import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    """
    Custom password validator with additional security requirements.
    """
    
    def validate(self, password, user=None):
        """
        Validate the password against custom rules.
        """
        errors = []
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            errors.append(
                ValidationError(
                    _('Password must contain at least one uppercase letter.'),
                    code='password_no_upper',
                )
            )
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            errors.append(
                ValidationError(
                    _('Password must contain at least one lowercase letter.'),
                    code='password_no_lower',
                )
            )
        
        # Check for at least one digit
        if not re.search(r'\d', password):
            errors.append(
                ValidationError(
                    _('Password must contain at least one digit.'),
                    code='password_no_digit',
                )
            )
        
        if errors:
            raise ValidationError(errors)
    
    def get_help_text(self):
        return _(
            'Your password must contain at least one uppercase letter, '
            'one lowercase letter, and one digit.'
        )