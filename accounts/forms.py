"""Accounts Forms."""

from django import forms

from . import models

import re

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, UserAttributeSimilarityValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.db.models import TextField
from django.forms import DateField
from django.contrib.auth.hashers import check_password

# ---Signup form
class SignUpForm(UserCreationForm):
    """Define the SignUpForm which extends UserCreationForm"""
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    verify_email = forms.EmailField(
        required=True,
        label="Confirm email:",
        help_text='Enter the same email as before, for verification.'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'verify_email',
            'password1',
            'password2',
        )

    def clean(self):
        """Confirm the emails match"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify = cleaned_data.get('verify_email')
        if email != verify:
            raise ValidationError("Emails do not match.")
        return cleaned_data
# ---/Signup form


# ---Edit User form
class EditUserForm(forms.ModelForm):
    """Define the Edit User Form."""
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)


    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )
# ---/Edit User form


# ---Edit Email form
class EditEmailForm(forms.ModelForm):
    """Define the Edit User Form."""
    email = forms.EmailField(
        required=True,
        label="Enter your new email address:")
    verify_email = forms.EmailField(
        required=True,
        label="Confirm email:",
        help_text='Enter the same email as before, for verification.'
     )

    class Meta:
        model = User
        fields = (
            'email',
            'verify_email',
        )

    def clean(self):
        """Confirm the emails match"""
        cleaned_data =  super().clean()
        email = cleaned_data.get('email')
        verify = cleaned_data.get('verify_email')
        if email != verify:
            raise ValidationError("Emails do not match.")
        return cleaned_data
# ---/Edit User form


# ---Profile form
class ProfileForm(forms.ModelForm):
    """Define the Profile Form."""

    # def clean_dob(self):
    #     """Vaidate the D.O.B. format"""
    #     raise forms.ValidationError("This is a test Validation Error message")
    #     return self

    def clean_bio(self):
        """Validate the bio field"""
        bio = self.cleaned_data['bio']
        if len(bio) < 10:
            raise ValidationError("Bio must contain at least 10 characters.")
        return bio

    date_of_birth = DateField(
        error_messages={'invalid': 'Date should be in one of the following formats: '
                                   'YYYY-MM-DD or MM/DD/YYY or MM/DD/YY'},
        label="Date of birth (YYYY-MM-DD or MM/DD/YYY or MM/DD/YY)"
    )

    bio = TextField(validators=[clean_bio])

    class Meta:
        model = models.Profile
        fields = (
            'city',
            'county',
            'country',
            'date_of_birth',
            'bio',
            'interests',
            'website',
        )

        labels = {
            'bio': 'Short biography',
            'county': 'State / County',
            'interests': "Interests (optional)",
            'website': "Website (optional)",
        }
# ---/Profile form


# ---Avatar form
class AvatarForm(forms.ModelForm):
    """Define the Avatar Form."""

    class Meta:
        model = models.Profile
        fields = ('avatar', )

        labels = {
            'avatar': '',
        }
# ---/Avatar form


# ---Validators
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


class ChangedValidator(object):
    def __init__(self, user):
        self.user = user

    def __call__(self, value):
        if check_password(value, self.user.password):
            raise ValidationError(
                _("The new password must be differnet from the old one."),
                code='password_not_changed'
            )
# ---/Validators


# ---Change Password form
class ChangePasswordForm(forms.Form):
    """Define the Edit User Form."""

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields["new_password"].validators.append(ChangedValidator(user))

    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    #     super(ChangePasswordForm, self).__init__(*args, **kwargs)

    current_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True, validators=[
        validate_password,
        MixcaseValidator,
        NumberValidator,
        SpecialCharacterValidator,
    ])
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm new password",)



    def clean(self):
        """Validate that the emails match"""
        cleaned_data = super().clean()
        new_password = self.data['new_password']
        confirm_password = cleaned_data['confirm_password']
        MatchValidator().validate(new_password, confirm_password)  # Check that the passwords match
        UserAttributeSimilarityValidator(user_attributes=[  # Check for user attribute simarlarity
                                        'username',
                                        'first_name',
                                        'last_name', ], max_similarity=0.4
                                        ).validate(new_password, user=self.user)

        return cleaned_data
# ---/Change Password form


# ---Custom Validators
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