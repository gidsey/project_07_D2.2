"""Accounts Forms."""

from django import forms
from PIL import Image

from . import models
from . import validators

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.db.models import TextField
from django.forms import DateField
from django_summernote.widgets import SummernoteInplaceWidget


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
        """Validate that the emails match"""
        cleaned_data = super().clean()
        validators.EmailMatchValidator().validate(cleaned_data['email'], cleaned_data['verify_email'])
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
        """Validate that the emails match"""
        cleaned_data = super().clean()
        validators.EmailMatchValidator().validate(cleaned_data['email'], cleaned_data['verify_email'])
        return cleaned_data
# ---/Edit User form


# ---Profile form
class ProfileForm(forms.ModelForm):
    """Define the Profile Form."""

    def clean_bio(self):
        """Validate the bio field"""
        bio = self.cleaned_data['bio']
        if len(bio) < 10:
            raise ValidationError('Biography must contain at least 10 characters.')
        return bio

    date_of_birth = DateField(
        error_messages={'invalid': 'Date should be in one of the following formats: '
                                   'YYYY-MM-DD or MM/DD/YYY or MM/DD/YY'},
        label="Date of birth",
    )

    bio = TextField(validators=[clean_bio])

    class Meta:
        model = models.Profile

        fields = (
            'date_of_birth',
            'city',
            'county',
            'country',
            'bio',
            'interests',
            'website',
        )
        widgets = {
            'bio': SummernoteInplaceWidget(),
            'interests': SummernoteInplaceWidget(),
        }
        labels = {
            'bio': 'Biography',
            'county': 'State / County (optional)',
            'interests': "Interests (optional)",
            'website': "Website (optional)",
        }
# ---/Profile form


# ---Avatar form
class AvatarForm(forms.ModelForm):
    """Define the Avatar Form."""
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = models.Profile
        fields = ('file', 'x', 'y', 'width', 'height', )
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }

    def save(self):
        photo = super(AvatarForm, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo
# ---/Avatar form


# ---Change Password form
class ChangePasswordForm(forms.Form):
    """Define the Edit User Form."""

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields["current_password"].validators.append(validators.CurrentPasswordValidator(user))
        self.fields["new_password"].validators.append(validators.ChangedValidator(user))
        self.fields["new_password"].validators.append(validators.SimilarValidator(user))

    current_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True, validators=[
        validate_password,
        validators.MixcaseValidator,
        validators.NumberValidator,
        validators.SpecialCharacterValidator,
    ])
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True,
                                       label="Confirm new password",)

    def clean(self):
        """Validate that the emails match"""
        cleaned_data = super().clean()
        validators.PasswordMatchValidator().validate(self.data['new_password'], cleaned_data['confirm_password'])
        return cleaned_data
# ---/Change Password form


