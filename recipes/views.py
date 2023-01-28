from django.shortcuts import render
from django.views.generic.base import View
from .models import Recipe

# Відображення всіх рецептів на головній сторінці

class RecipeView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        return render(request, 'recipes/index.html', {'recipes_list': recipes})

# Відображення сторінки кокретного рецепту

class RecipeDetail(View):
    def get(self, request, pk):
        recipe = Recipe.objects.get(id=pk)
        return render(request, 'recipes/recipe.html', {'recipe': recipe})
