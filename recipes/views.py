from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from .models import Recipe, StarRating
from .forms import CommentForm

# Display of all existing recipes

class RecipeView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        return render(request, 'recipes/index.html', {'recipes_list': recipes})

# Display the specific recipe page

class RecipeDetail(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            recipe = Recipe.objects.get(id=pk)
            try:
                rating = StarRating.objects.get(user=request.user, recipe=recipe)
            except StarRating.DoesNotExist:
                rating = None
            return render(request, 'recipes/recipe.html', {'recipe': recipe, 'rating': rating})
        else:
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

# Like recipe on the recipe page

class LikeRecipe(View):
    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, id=request.POST.get('recipe_id'))
        if recipe.likes.filter(id=request.user.id).exists():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)
        return redirect(f'/{pk}')
    
class RateStar(View):
    def get(self, request, recipe_id, rating):
        recipe = Recipe.objects.get(id=recipe_id)
        StarRating.objects.filter(recipe=recipe, user=request.user).delete()
        StarRating.objects.create(recipe=recipe, user=request.user, rating=rating)
        return render(request, "recipes/recipe.html", {"recipe": recipe})