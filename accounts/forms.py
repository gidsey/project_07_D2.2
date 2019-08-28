"""Accounts Forms."""

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from . import models


class SignUpForm(UserCreationForm):
    """Define the SignUpForm which extends UserCreationForm"""
    verify_email = forms.EmailField(
        required=True,
        label="Email confirmation:",
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
        """Clean the form"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify = cleaned_data.get('verify_email')

        if email != verify:  # Verify that the emails match.
            raise ValidationError(
                "Emails do not match"
            )


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = (
#             'first_name',
#             'last_name',
#             'email',
#         )

class ProfileForm(forms.ModelForm):
    """Define the Profile Form."""

    class Meta:
        model = models.Profile
        fields = (
            'user',
            'first_name',
            'last_name',
            'email',
            'verify_email',
            'date_of_birth',
            'bio',
            'avatar',
            'city',
            'county',
            'country',
            'interests',
            'website',
        )
        exclude = ('user',)
        labels = {
            'bio': 'Bio (optional) ',
        }
        help_texts = {
            'verify_email': 'Enter the same email as before, for verification.'
        }


    # def clean(self):
    #     """Clean the form"""
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get('email')
    #     verify = cleaned_data.get('verify_email')
    #
    #     if email != verify:  # Verify that the emails match.
    #         raise ValidationError(
    #             "Emails do not match"
    #         )
