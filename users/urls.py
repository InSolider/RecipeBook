from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.user_signin_signup, name='signin'),
    path('signout', views.user_signout, name='signout'),
    path('user/<int:pk>/edit-profile', views.EditProfileView.as_view(), name='edit_profile'),
    path('user/<int:pk>/edit-email', views.EditEmailView.as_view(), name='edit_email'),
    path('user/<int:pk>/change-password', views.ChangePasswordView.as_view(template_name='users/change_password.html'), name='change_password'),
]