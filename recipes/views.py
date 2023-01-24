from django.shortcuts import render
from django.views.generic.base import View
from .models import Recipe

# Відображення рецептів

class RecipeView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        return render(request, 'recipes/index.html', {'recipes_list': recipes})
