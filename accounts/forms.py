"""Accounts Forms."""
from django import forms
from django.contrib.auth.models import User
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
            # 'date_of_birth',
            'bio',
            'avatar',
            'city',
            'county',
            'country',
            'interests',
            'website',
        )
        exclude = ('user', )
