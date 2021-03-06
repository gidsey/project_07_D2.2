from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from . models import Profile

class ProfileInline(admin.StackedInline):
    """Define inline admin for Profile."""

    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    """Define a new User admin."""

    inlines = (ProfileInline, )

# Re-register UserAdmin


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
