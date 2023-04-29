# Generated by Django 4.1.7 on 2023-04-03 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms
import recipes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Назва')),
                ('amount', models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Кількість')),
                ('unit', models.CharField(choices=[('kg', 'кг.'), ('l', 'л.'), ('p', 'шт.')], default='kg', max_length=2, verbose_name='Одиниця вимірювання')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Ціна')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Дата редагування')),
            ],
            options={
                'verbose_name': 'Інгрідієнт',
                'verbose_name_plural': 'Інгрідієнти',
                'db_table': 'Ingredients',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Назва')),
                ('description', models.TextField(verbose_name='Розгорнутий рецепт')),
                ('cooking_time', models.CharField(max_length=32, verbose_name='Час приготування')),
                ('author', models.CharField(max_length=64, verbose_name='Автор')),
                ('total_worth', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Загальна вартість')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата публікації')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Дата редагування')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепти',
                'db_table': 'Recipes',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=3, max_digits=5, verbose_name='Кількість (кг./л./шт.)')),
                ('worth', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Вартість')),
                ('ingredient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.ingredient', verbose_name='Інгрідієнт')),
                ('recipe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.recipe')),
            ],
            options={
                'verbose_name': 'Інгрідієнт',
                'verbose_name_plural': 'Інгрідієнти для страви',
                'db_table': 'IngredientsInRecipes',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Дата публікації')),
                ('content', models.TextField(max_length=2000, verbose_name='Вміст')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Коментар до рецепту')),
                ('сommented_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Коментар',
                'verbose_name_plural': 'Коментарі',
                'db_table': 'Comments',
            },
        ),
    ]
