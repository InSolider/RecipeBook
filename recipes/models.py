from django.db import models
from django.utils.timezone import localtime
from django.template.defaultfilters import date as dateconvert
from django_resized import ResizedImageField
from translitua import translit
from django_currentuser.db.models import CurrentUserField
from django.db.models import Sum

# Database model for recipes

class Recipe(models.Model):
    
    def get_preview_path(self, filename):
        path = 'images/' + dateconvert(localtime(self.created), 'ymd-Hi-') + translit(self.title).replace(' ', '-') + '/cover.webp'
        return path
    
    preview = ResizedImageField(verbose_name='Фото-прев\'ю', upload_to=get_preview_path, size=[1920, 1080], crop=['middle', 'center'], quality=100, force_format='WEBP')
    title = models.CharField('Назва', max_length=128)
    description = models.TextField('Розгорнутий рецепт')
    cooking_time = models.CharField('Час приготування', max_length=32)
    author = models.CharField('Автор', max_length=64)
    total_worth = models.DecimalField('Загальна вартість', max_digits=6, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField('Дата публікації', auto_now_add=True)
    modified = models.DateTimeField('Дата редагування', auto_now=True)

    def __str__(self):
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        self.total_worth = RecipeIngredient.objects.aggregate(Sum('worth'))['worth__sum']
        super().save(*args, **kwargs)

    class Meta:
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
    modified_by = CurrentUserField(verbose_name='Відредагував', on_update=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Інгрідієнт'
        verbose_name_plural = 'Інгрідієнти'

# Database model for ingredients in recipes

class RecipeIngredient(models.Model):
    
    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True, verbose_name='Інгрідієнт')
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
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
        verbose_name = 'Інгрідієнт'
        verbose_name_plural = 'Інгрідієнти для страви'