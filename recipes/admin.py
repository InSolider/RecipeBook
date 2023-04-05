from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredient, Comment

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    readonly_fields = ['worth']

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'unit', 'price', 'modified', 'modified_by']
    readonly_fields = ['modified_by']

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['title', 'created_by', 'created', 'modified_by', 'modified']
    readonly_fields = ['created_by', 'modified_by', 'likes']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'сommented_by', 'created_on', 'content']
    readonly_fields = ['recipe', 'сommented_by']
