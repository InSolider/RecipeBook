from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredient, Comment

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    readonly_fields = ['worth']

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'unit', 'price', 'modified', 'modified_by']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['title', 'author', 'modified', 'created']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'сommented_by', 'created_on', 'content']
    readonly_fields = ['recipe', 'сommented_by']
