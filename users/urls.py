from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.user_signin_signup, name='signin'),
    path('signout', views.user_signout, name='signout'),
    path('id<int:pk>/edit-profile/', views.EditProfile.as_view(), name='edit_profile'),
]