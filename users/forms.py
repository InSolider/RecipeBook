from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.validators import MaxLengthValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django import forms
from .models import Profile

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

class EditProfileForm(forms.ModelForm):
    gender_choices=[
        ('n', 'Не скажу'),
        ('m', 'Чоловіча'),
        ('f', 'Жіноча'),
    ]
    
    gender = forms.ChoiceField(label='Стать', choices=gender_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(label='День народження', widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control'}))
    bio = forms.CharField(label='Розкажіть щось про себе', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))

    class Meta:
        model = Profile
        fields = ('gender', 'birth_date', 'bio')

class EditUsernameForm(forms.ModelForm):
    username = forms.CharField(label='Ім\'я користувача', widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = get_user_model()
        fields = ('username', )

class EditEmailForm(forms.ModelForm):
    first_name = forms.CharField(label='Ім\'я', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Електронна пошта', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}))

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'email')

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старий пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Новий пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Новий пароль ще раз', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password2')