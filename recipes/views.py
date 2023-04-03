from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import Recipe
from .forms import CommentForm

# Display of all existing recipes

class RecipeView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        return render(request, 'recipes/index.html', {'recipes_list': recipes})

# Displaying the specific recipe page

class RecipeDetail(View):
    def get(self, request, pk):
        recipe = Recipe.objects.get(id=pk)
        return render(request, 'recipes/recipe.html', {'recipe': recipe})
    
# Adding a comment on the recipe page

class AddComment(View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.recipe_id = pk
            form.сommented_by = request.user
            form.save()
        return redirect(f'/{pk}')