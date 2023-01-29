from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeView.as_view(), name='home'),
    path('<int:pk>/', views.RecipeDetail.as_view()),
]