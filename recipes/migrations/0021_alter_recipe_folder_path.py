# Generated by Django 4.2 on 2023-04-28 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0020_alter_recipe_folder_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='folder_path',
            field=models.FilePathField(blank=True, max_length=260, null=True, verbose_name='Шлях до папки'),
        ),
    ]
