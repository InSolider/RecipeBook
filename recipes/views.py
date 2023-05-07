from django.db.models import Count
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from .forms import CommentForm
from .models import Recipe, Ingredient, StarRating, Category

# Display of all existing recipes on home page
class RecipeView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        ingredients = Ingredient.objects.all().order_by('name')
        categories = Category.objects.all()
        return render(request, 'recipes/index.html', {'recipes': recipes, 'ingredients': ingredients, 'categories': categories})
    
    def post(self, request):
        ingredients = Ingredient.objects.all().order_by('name')
        categories = Category.objects.all()
        selected_ingredients = []
        for ingredient in ingredients:
            if request.POST.get(ingredient.name):
                selected_ingredients.append(ingredient.name)
        if len(selected_ingredients) == 0:
            recipes = Recipe.objects.all()
        else:
            recipes = Recipe.objects.filter(recipeingredient__ingredient__name__in=selected_ingredients).annotate(num_ingredients=Count('recipeingredient')).filter(num_ingredients=len(selected_ingredients))
        return render(request, 'recipes/index.html', {'recipes': recipes, 'ingredients': ingredients, 'selected_ingredients': selected_ingredients, 'categories': categories})

# Display the specific recipe page
class RecipeDetail(View):
    def get(self, request, slug):
        recipe = Recipe.objects.get(slug=slug)
        categories = Category.objects.all()
        if request.user.is_authenticated:
            try:
                rating = StarRating.objects.get(user=request.user, recipe=recipe)
            except StarRating.DoesNotExist:
                rating = None
            return render(request, 'recipes/recipe.html', {'recipe': recipe, 'rating': rating, 'categories': categories})
        else:
            return render(request, 'recipes/recipe.html', {'recipe': recipe, 'categories': categories})
        
# Add comment on the specific recipe page
class AddComment(LoginRequiredMixin, View):
    def get(self, request, slug):
        recipe = Recipe.objects.get(slug=slug)
        return render(request, 'recipes/recipe.html', {'recipe': recipe})

    def post(self, request, slug):
        form = CommentForm(request.POST)
        recipe = Recipe.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            form.recipe_id = recipe.id
            form.сommented_by = request.user
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, 'recipes/recipe.html', {'recipe': recipe})

# Like recipe on the specific recipe page
class LikeRecipe(LoginRequiredMixin, View):
    def get(self, request, slug):
        recipe = Recipe.objects.get(slug=slug)
        return render(request, 'recipes/recipe.html', {'recipe': recipe})

    def post(self, request, slug):
        recipe = Recipe.objects.get(slug=slug)
        if recipe.likes.filter(id=request.user.id).exists():
            recipe.likes.remove(request.user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            recipe.likes.add(request.user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, 'recipes/recipe.html', {'recipe': recipe})
        
# Rate recipe on the specific recipe page
class RateStar(LoginRequiredMixin, View):
    def get(self, request, recipe_id, rating):
        recipe = Recipe.objects.get(id=recipe_id)
        StarRating.objects.filter(recipe=recipe, user=request.user).delete()
        StarRating.objects.create(recipe=recipe, user=request.user, rating=rating)
        return render(request, "recipes/recipe.html", {"recipe": recipe})

# Search recipes
class SearchResult(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "recipes/search_result.html", {'categories': categories})
    
    def post(self, request):
        searched = request.POST['searched']
        searching_recipes = Recipe.objects.filter(title__iregex=searched)
        categories = Category.objects.all()
        return render(request, "recipes/search_result.html", {'searched': searched, 'searching_recipes': searching_recipes, 'categories': categories})

# Show favorites recipes
class FavoritesRecipes(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        favorites_recipes = user.like_recipe.all()
        categories = Category.objects.all()
        return render(request, "recipes/favorites.html", {'favorites_recipes': favorites_recipes, 'categories': categories})

# Show recipes by category
class CategoryRecipes(View):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        category_recipes = Recipe.objects.filter(category__name=category.name)
        categories = Category.objects.all()
        return render(request, "recipes/category.html", {'category_recipes': category_recipes, 'category': category, 'categories': categories})