"""Custom validators."""

from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

import re


# ---Validator functions
def MixcaseValidator(value):
    if value.islower() or value.isupper():
        raise ValidationError(
            _("The password must contain both lower and uppercase characters."),
            params={'value': value},
        )


def NumberValidator(value):
    """Validate that password contains at least one numerical digit."""
    numbers = re.findall(r'\d', value)
    if not numbers:
        raise ValidationError(
            _("The password must contain at least one number."),
            params={'value': value},
        )


def SpecialCharacterValidator(value):
    """Validate that password contains at least one numerical digit."""
    numbers = re.findall(r'[@#$%^&*£\-+]', value)
    if not numbers:
        raise ValidationError(
            _("The password must contain at least one special character (e.g. @ # $ % ^ & *)."),
            code='password_no_specials'
        )
# ---/Validator functions


# ---Custom Validators
class ChangedValidator(object):
    def __init__(self, user):
        self.user = user

    def __call__(self, value):
        if check_password(value, self.user.password):
            raise ValidationError(
                _("The new password must be differnet from the old one."),
                code='password_not_changed'
            )


class MatchValidator:
    """Validate the password and confirm password match."""
    def validate(self, password, confirm_password):
        if password != confirm_password:
            raise ValidationError(
                _("Passwords do not match."),
                code='passwords_not_matching'
                )

    def get_help_text(self):
        return (
            "Enter the same password again for confirmation."
        )
# ---/Custom Validators
