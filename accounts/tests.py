from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User

from . import forms

client = Client()


class TestRestrictedAccess(TestCase):
    """ Test anonymous access to restricted pages."""

    def test_anonymous_user_profile(self):
        """Test anonymous access to profile page is redirected."""
        response = client.get(reverse('accounts:profile'))
        self.assertNotEqual(response.status_code, 200)

    def test_anonymous_user_create_profile(self):
        """Test anonymous access to create profile page is redirected."""
        response = client.get(reverse('accounts:create_profile'))
        self.assertNotEqual(response.status_code, 200)

    def test_anonymous_user_edit_profile(self):
        """Test anonymous access to edit profile page is redirected."""
        response = client.get(reverse('accounts:edit_profile'))
        self.assertNotEqual(response.status_code, 200)

    def test_anonymous_user_change_password(self):
        """Test anonymous access to change password page is redirected."""
        response = client.get(reverse('accounts:change_password'))
        self.assertNotEqual(response.status_code, 200)


class TestProfile(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='EcoWarrior101',
            first_name='Dave',
            last_name="Angel",
            email='dave.angel@mailinator.com',
            password='m00nlight$hadow3',
        )
        login = self.client.login(username='EcoWarrior101', password='m00nlight$hadow3',)

    def test_sign_in(self):
        """Test user creation."""
        response = self.client.get(reverse('accounts:sign_in'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/sign_in.html')

    def test_profile(self):
        """Test logged-in access to the view profile page."""
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_create_profile(self):
        """Test logged-in access to the create profile page."""
        response = self.client.get(reverse('accounts:create_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/create_profile.html')

    def test_edit_profile(self):
        """Test logged-in access to the edit profile page."""
        response = self.client.get(reverse('accounts:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit_profile.html')

    def test_change_password_form(self):
        """Test the positive form validation for change passowrd."""
        form_data = {
            'current_password': 'm00nlight$hadow3',
            'new_password': 'Pa$$w0rd!Pa$$w0rd!7',
            'confirm_password': 'Pa$$w0rd!Pa$$w0rd!7',
        }
        form = forms.ChangePasswordForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_change_password_form_fail(self):
        """Test the negative form validation for change passowrd."""
        form_data = {
            'current_password': 'm00nlight$hadow3',
            'new_password': 'DaveAngel77%66',
            'confirm_password': 'DaveAngel77%66',
        }
        form = forms.ChangePasswordForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())

    def test_profile_form(self):
        """Test the profile form."""
        form_data = {
            'date_of_birth': '1980-02-03',
            'city': 'Basildon',
            'county': "Essex",
            'country': 'UK',
            'bio': "A classic Essex geezer who, despite his get-up and rather lavish lifestyle, is improbably "
                   "concerned about saving the planet (though this is often undermined by his wife's behaviour), "
                   "Mike Oldfield records, and Swinging. 'Moonlight Shadow' by Mike Oldfield and Maggie Reilly is "
                   "used as the theme tune to sketches featuring this character",
            'interets': 'Mike Oldfield, saving the planet',
            'website': 'https://en.wikipedia.org/wiki/The_Fast_Show',
        }
        form = forms.ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_profile_form_fail(self):
        """Test the profile form."""
        form_data = {
            'date_of_birth': '1980-02-03',
            'city': 'Basildon',
            'county': "Essex",
            'country': 'UK',
            'bio': "A classic",
            'interets': 'Mike Oldfield, saving the planet',
            'website': 'https://en.wikipedia.org/wiki/The_Fast_Show',
        }
        form = forms.ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())