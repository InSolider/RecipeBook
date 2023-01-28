from django.db import models
from django.utils.timezone import localtime
from django.template.defaultfilters import date as dateconvert
from django_resized import ResizedImageField
from translitua import translit

#Дані про рецепт у БД

class Recipe(models.Model):
    
    def get_preview_path(self, filename):
        path = 'images/' + dateconvert(localtime(self.created), 'ymd-Hi-') + translit(self.title).replace(' ', '-') + '/cover.webp'
        return path
    
    preview = ResizedImageField(upload_to=get_preview_path, size=[1920, 1080], crop=['middle', 'center'], quality=100, force_format='WEBP')
    title = models.CharField('Назва', max_length=100)
    description = models.TextField('Рецепт')
    cooking_time = models.CharField('Час приготування', max_length=15)
    author = models.CharField('Автор', max_length=100)
    created = models.DateTimeField('Дата публікації', auto_now_add=True)
    modified = models.DateTimeField('Дата редагування', auto_now=True)

    def __str__(self):
        return f'{self.title}, {self.author}, {self. modified}, {self. created}'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепти'
