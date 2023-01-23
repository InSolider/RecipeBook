from django.db import models

#Дані про рецепт 

class Recipe(models.Model):
    title = models.CharField('Назва рецепту', max_length=100)
    description = models.TextField('Покроковий рецепт')
    author = models.CharField('Ім\'я автора', max_length=100)
    date = models.DateTimeField('Дата публікації')

    def __str__(self):
        return f'{self.title}, {self.author}, {self.date}'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепти'
