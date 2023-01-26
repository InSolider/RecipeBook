from django.db import models

#Дані про рецепт у БД

class Recipe(models.Model):
    preview = models.ImageField('Прев\'ю', upload_to='images/')
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
