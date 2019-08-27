"""Accounts Forms."""
import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from . import models


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')


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


    def clean(self):
        """Clean the form"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify = cleaned_data.get('verify_email')
        # date_of_birth = cleaned_data.get('date_of_birth')

        if email != verify:  # Verify that the emails match.
            raise ValidationError(
                "Emails do not match"
            )

        # if date_of_birth != datetime:  # Verify the date is valid.
        #     raise ValidationError(
        #         "Please enter a valid date"
        #     )
