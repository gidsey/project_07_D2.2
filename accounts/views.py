from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms
from . import models


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('home')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "Account setup successully! You've been signed in too."
            )
            return HttpResponseRedirect(reverse('accounts:create_profile'))

    return render(request, 'accounts/sign_up.html', {
        'form': form,
    })


@login_required
def create_profile(request):
    """Propulate the Profile after the user has been created."""
    profile_form = forms.ProfileForm()
    user = request.user
    if request.method == 'POST':
        try:
            user.profile = request.user.profile  # Set Profile instance for the current user
        except models.Profile.DoesNotExist:
            user.profile = models.Profile(user=request.user)  # Set the Profile instance for new user

        profile_form = forms.ProfileForm(data=request.POST, instance=user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(
                request,
                "Profile saved successully."
            )
            return HttpResponseRedirect(reverse('accounts:profile'))

    return render(request, 'accounts/create_profile.html', {
        'profile_form': profile_form,
    })


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required(login_url='accounts/sign_in/')
def profile(request):
    """Define the Profile view"""
    avatar_form = forms.AvatarForm()
    user = request.user
    # if not request.user.profile.avatar:  # Use default image if no avatar set
    #     request.user.profile.avatar = 'placeholder/default.png'

    if request.method == 'POST':
        user.profile = request.user.profile
        avatar_form = forms.AvatarForm(data=request.POST, files=request.FILES, instance=user.profile)
        if avatar_form.is_valid():

            avatar_form.save()

            messages.success(request,
                             "Avatar uploaded successully."
                             )
        return HttpResponseRedirect(reverse('accounts:profile'))

    return render(request, 'accounts/profile.html', {
        'current_user': request.user,
        'avatar_form': avatar_form,
    })


@login_required(login_url='accounts/sign_in/')
def edit_profile(request):
    """Define the Edit Profile view"""
    user = request.user
    form = forms.EditUserForm(instance=user)
    email_form = forms.EditEmailForm(instance=user)
    profile_form = forms.ProfileForm(instance=user.profile)
    if request.method == 'POST':
        if 'update_name' in request.POST:
            form = forms.EditUserForm(data=request.POST, instance=user)
            profile_form = forms.ProfileForm(data=request.POST, instance=user.profile)
            if form.is_valid() and profile_form.is_valid():
                form.save()
                profile_form.save()
                messages.success(request, "Profile updated successully.")
                return HttpResponseRedirect(reverse('accounts:profile'))

        elif 'update_email' in request.POST:
            email_form = forms.EditEmailForm(data=request.POST, instance=user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Email updated successully.")
                return HttpResponseRedirect(reverse('accounts:profile'))
            else:
                return render(request, 'accounts/edit_profile.html', {
                    'current_user': user,
                    'form': form,
                    'email_form': email_form,
                    'collapse': 'false',  # Keep the email panel open to show errors
                })

    return render(request, 'accounts/edit_profile.html', {
        'current_user': user,
        'form': form,
        'email_form': email_form,
        'profile_form':  profile_form,
    })


@login_required(login_url='accounts/sign_in/')
def change_password(request):
    """Define the change password view."""
    user = request.user
    change_password_form = forms.ChangePasswordForm(request.user)
    if request.method == 'POST':
        change_password_form = forms.ChangePasswordForm(request.user, data=request.POST)
        if change_password_form.is_valid():
            user.set_password(change_password_form.cleaned_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully.")
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/change_password.html', {
        'current_user': user,
        'change_password_form': change_password_form,
    })
