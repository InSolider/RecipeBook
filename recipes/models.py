from django.db import models
from django.conf import settings
from django.db.models import Avg
from django.utils.timezone import localtime
from django.template.defaultfilters import date

from translitua import translit
from django_resized import ResizedImageField
from django_ckeditor_5.fields import CKEditor5Field

# Database model for categories
class Category(models.Model):

    name = models.CharField('Назва', max_length=50, unique=True)
    slug = models.CharField('Посилання', max_length=64)

    def save(self, *args, **kwargs):
        self.slug = translit(self.name).lower().replace(' ', '-')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'Categories'
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

# Database model for recipes
class Recipe(models.Model):
    
    def get_preview_path(self, filename):
        path = 'images\\' + date(localtime(self.created), 'ymd-Hi-') + translit(self.title).replace(' ', '-') + '/cover.webp'
        return path
    
    def update_total_price(self):
        self.total_price = 0
        for i in RecipeIngredient.objects.filter(recipe=self):
            self.total_price += i.quantity / i.ingredient.amount * i.ingredient.price
        self.save()

    def average_rating(self) -> float:
        self.avg_rating = StarRating.objects.filter(recipe=self).aggregate(Avg("rating"))["rating__avg"] or 5
        self.save()

    preview = ResizedImageField(verbose_name='Фото-прев\'ю', upload_to=get_preview_path, size=[1920, 1080], crop=['middle', 'center'], quality=100, force_format='WEBP')
    folder_path = models.FilePathField('Шлях до папки з фото', max_length=128)
    title = models.CharField('Назва', max_length=100, unique=True)
    slug = models.CharField('Посилання', max_length=128)
    description = CKEditor5Field('Детальний рецепт', config_name='extends')
    cooking_time = models.CharField('Час приготування', max_length=30)
    portions = models.IntegerField('Кількість порцій')
    created = models.DateTimeField('Дата публікації', auto_now_add=True)
    modified = models.DateTimeField('Дата редагування', auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Уподобали', related_name='like_recipe')
    total_price = models.DecimalField('Вартість', max_digits=6, decimal_places=2, null=True)
    avg_rating = models.DecimalField('Оцінка', max_digits=2, decimal_places=1, default=5)
    category = models.ManyToManyField(Category, verbose_name='Категорії')

    def __str__(self):
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.folder_path = 'images\\' + date(localtime(self.created), 'ymd-Hi-') + translit(self.title).replace(' ', '-')
        self.slug = translit(self.title).lower().replace(' ', '-')
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'Recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепти'

# Database model for ingredients
class Ingredient(models.Model):

    name = models.CharField('Назва', max_length=50, unique=True)
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
    worth = models.DecimalField('Вартість', max_digits=6, decimal_places=2)

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
    content = models.TextField('Вміст', max_length=1000)

    def __str__(self):
        return f'Коментар залишений користувачем "{self.сommented_by}" до рецепту "{self.recipe}" в {localtime(self.created_on).strftime("%H:%M:%S %d.%m.%Y")}'
    
    class Meta:
        db_table = 'Comments'
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'

# Database model for stars rate
class StarRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Користувач', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт', on_delete=models.CASCADE)
    rating = models.IntegerField('Оцінка', default=0)

    def __str__(self):
        return f'Оцінка користувача {self.user} до рецепту "{self.recipe}"'
    
    class Meta:
        db_table = 'StarRatings'
        verbose_name = 'Оцінка'
        verbose_name_plural = 'Оцінки'    