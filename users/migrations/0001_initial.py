# Generated by Django 4.2 on 2023-04-06 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('n', 'Не скажу'), ('m', 'Чоловіча'), ('f', 'Жіноча')], default='n', max_length=2, verbose_name='Стать')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата народження')),
                ('bio', models.TextField(blank=True, max_length=512, null=True, verbose_name='Про Вас')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
