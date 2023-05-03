from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeView.as_view(), name='home'),
    path('<int:pk>/', views.RecipeDetail.as_view()),
    path('comments/<int:pk>/', views.AddComment.as_view(), name='add_comment'),
    path('likes/<int:pk>/', views.LikeRecipe.as_view(), name='like_recipe'),
    path('rate/<int:recipe_id>/<int:rating>/', views.RateStar.as_view()),
]