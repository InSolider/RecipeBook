from django.apps import AppConfig

class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'

class IngredientsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ingredients'

class RecipeIngredientsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipeingredients'