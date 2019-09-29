from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User

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



