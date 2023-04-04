from django.db import models
from django.conf import settings
from django.utils.timezone import localtime
from django.template.defaultfilters import date
from django_resized import ResizedImageField
from translitua import translit

# Database model for recipes

class Recipe(models.Model):
    
    def get_preview_path(self, filename):
        path = 'images/' + date(localtime(self.created), 'ymd-Hi-') + translit(self.title).replace(' ', '-') + '/cover.webp'
        return path
    
    preview = ResizedImageField(verbose_name='Фото-прев\'ю', upload_to=get_preview_path, size=[1920, 1080], crop=['middle', 'center'], quality=100, force_format='WEBP')
    title = models.CharField('Назва', max_length=128)
    description = models.TextField('Розгорнутий рецепт')
    cooking_time = models.CharField('Час приготування', max_length=32)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', related_name='recipe_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField('Дата публікації', auto_now_add=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Відредагував', related_name='recipe_modified_by', null=True, blank=True, on_delete=models.SET_NULL)
    modified = models.DateTimeField('Дата редагування', auto_now=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'Recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепти'

# Database model for ingredients

class Ingredient(models.Model):

    name = models.CharField('Назва', max_length=64)
    amount = models.DecimalField('Кількість', max_digits=5, decimal_places=3)
    unit = models.CharField('Одиниця вимірювання',
        max_length=2,
        choices=[
        ('kg', 'кг.'),
        ('l', 'л.'),
        ('p', 'шт.'),
        ],
        default='kg',
    )
    price = models.DecimalField('Ціна', max_digits=6, decimal_places=2)
    modified = models.DateTimeField('Дата редагування', auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Відредагував', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = 'Ingredients'
        verbose_name = 'Інгрідієнт'
        verbose_name_plural = 'Інгрідієнти'

# Database model for ingredients in recipes

class RecipeIngredient(models.Model):
    
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Інгрідієнт')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.DecimalField('Кількість (кг./л./шт.)', max_digits=5, decimal_places=3)
    worth = models.DecimalField('Вартість', max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        if self.ingredient.unit == 'p':
            return f'{self.ingredient.name} {int(self.quantity)} шт.'
        elif self.ingredient.unit == 'l':
            if self.quantity < 1:
                return f'{self.ingredient.name} {int(self.quantity * 1000)} мл.'
            else:
                return f'{self.ingredient.name} {int(self.quantity)} л.'
        else:
            if self.quantity < 1:
                return f'{self.ingredient.name} {int(self.quantity * 1000)} г.'
            else:
                return f'{self.ingredient.name} {int(self.quantity)} кг.'
    
    def save(self, *args, **kwargs):
        self.worth = self.quantity / self.ingredient.amount * self.ingredient.price
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'IngredientsInRecipes'
        verbose_name = 'Інгрідієнт'
        verbose_name_plural = 'Інгрідієнти для страви'

# Database model for comments

class Comment(models.Model):

    recipe = models.ForeignKey(Recipe, verbose_name='Коментар до рецепту', on_delete=models.CASCADE)
    сommented_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Користувач', on_delete=models.CASCADE)
    created_on = models.DateTimeField('Дата публікації', auto_now_add=True)
    content = models.TextField('Вміст', max_length=2000)

    def __str__(self):
        return f'Коментар залишений користувачем "{self.сommented_by}" до рецепту "{self.recipe}" в {localtime(self.created_on).strftime("%H:%M:%S %d.%m.%Y")}'
    
    class Meta:
        db_table = 'Comments'
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
