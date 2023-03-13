from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import MaxLengthValidator

class CustomRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, label='Ім\'я користувача', validators=[MaxLengthValidator(16, message="Максимальна довжина імені користувача 16 символів.")])
    email = forms.EmailField(required=True, label='Електронна пошта')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Така пошта вже використовується.")
        return email
    
    def __init__(self, *args, **kwargs):
        super(CustomRegistrationForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.error_messages = {'required':'Рядок "{fieldname}" є обов\'язковим для заповнення.'.format(fieldname=field.label)}

    error_messages = {
        'password_mismatch': 'Паролі не збігаються.',
    }