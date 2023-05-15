from django.contrib import admin

from .models import Recipe, Ingredient, RecipeIngredient, Category, Comment, StarRating

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    readonly_fields = ['worth']

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'unit', 'price', 'modified']

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['title', 'created', 'modified', 'total_price', 'avg_rating']
    readonly_fields = ['total_price','avg_rating', 'folder_path', 'likes']
    exclude = ['slug']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'сommented_by', 'created_on', 'short_content']
    readonly_fields = ['recipe', 'сommented_by']

    def short_content(self, obj):
        return obj.content[:64] + '...' if len(obj.content) > 64 else obj.content
    short_content.short_description = 'Коментар'

@admin.register(StarRating)
class StarRateAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user', 'rating']
    readonly_fields = ['recipe', 'user', 'rating']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    exclude = ['slug']