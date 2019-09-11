"""Accounts Forms."""

from django import forms

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.db.models import TextField
from django.forms import DateField

from . import models


class SignUpForm(UserCreationForm):
    """Define the SignUpForm which extends UserCreationForm"""
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
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
        return cleaned_data


class EditUserForm(forms.ModelForm):
    """Define the Edit User Form."""
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    verify_email = forms.EmailField(
        required=True,
        label="Email confirmation:",
        help_text='Enter the same email as before, for verification.'
    )

    class Meta:
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

        exclude = (
            'username',
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
        return cleaned_data


class ProfileForm(forms.ModelForm):
    """Define the Profile Form."""

    def clean_dob(self):
        """Vaidate the D.O.B. format"""
        print('datein = {}'.format(self))
        raise forms.ValidationError("This is a test Validation Error message")
        return self

    def clean_bio(self):
        """Validate the bio field"""
        bio = self.cleaned_data['bio']
        if len(bio) < 10:
            raise ValidationError("Bio must contain at least 10 characters.")
        return bio

    date_of_birth = DateField(
        # validators=[clean_dob],
        error_messages={'invalid': 'Date å be entered in one of the following formats: '
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




class AvatarForm(forms.ModelForm):
    """Define the Avatar Form."""

    class Meta:
        model = models.Profile
        fields = ('avatar', )

        labels = {
            'avatar': '',
        }
