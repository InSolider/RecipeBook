from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Користувач', on_delete=models.CASCADE)
    gender = models.CharField('Стать',
        max_length=2,
        choices=[
        ('n', 'Не скажу'),
        ('m', 'Чоловіча'),
        ('f', 'Жіноча'),
        ],
        default='n',
    )
    birth_date = models.DateField('Дата народження', null=True, blank=True)
    bio = models.TextField('Про Вас', max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        db_table = 'Profiles'
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
