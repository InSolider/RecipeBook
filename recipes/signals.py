from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
import os
import shutil
from .models import Ingredient, RecipeIngredient, Recipe

@receiver(post_save, sender=Ingredient)
def update_recipes_after_changing_Ingredient(sender, instance, **kwargs):
    for i in RecipeIngredient.objects.filter(ingredient=instance):
        i.recipe.update_total_price()

@receiver(post_save, sender=RecipeIngredient)
def update_recipe_after_changing_RecipeIngredient(sender, instance, **kwargs):
    instance.recipe.update_total_price()

@receiver(pre_delete, sender=Recipe)
def delete_related_folder(sender, instance, **kwargs):
    if os.path.exists(os.path.join(settings.MEDIA_ROOT, instance.folder_path)):
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, instance.folder_path))