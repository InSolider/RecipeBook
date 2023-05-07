from django.urls import path

from . import views

urlpatterns = [
    path('', views.RecipeView.as_view(), name='home'),
    path('recipe/<str:slug>', views.RecipeDetail.as_view(), name='recipe_detail'),
    path('comments/<str:slug>/', views.AddComment.as_view(), name='add_comment'),
    path('likes/<str:slug>/', views.LikeRecipe.as_view(), name='like_recipe'),
    path('rate/<int:recipe_id>/<int:rating>/', views.RateStar.as_view()),
    path('search-result', views.SearchResult.as_view(), name='search_result'),
    path('favorites', views.FavoritesRecipes.as_view(), name='favorites_recipes'),
    path('category/<str:slug>', views.CategoryRecipes.as_view(), name='category_recipes'),
]