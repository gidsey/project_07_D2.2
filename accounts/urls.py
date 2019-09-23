from django.urls import path

from . import views
from . import avatar

app_name = "accounts"  # required when using namespace in URLS

urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile, name='profile'),
    path('profile/change_password', views.change_password, name='change_password'),

    path('profile/set_avatar', avatar.set_avatar, name='set_avavtar'),
    path('profile/rotate_90_cc', avatar.rotate_90_cc, name='rotate_90_cc'),

]
