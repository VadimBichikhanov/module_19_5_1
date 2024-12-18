from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import News

class RegistrationForm(UserCreationForm):
    age = forms.IntegerField(
        label="Возраст",
        help_text="Введите ваш возраст",
        min_value=18,  # Минимальный возраст
        max_value=120  # Максимальный возраст
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'age']

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age < 18:
            raise forms.ValidationError("Ваш возраст должен быть не менее 18 лет.")
        return age

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'date']
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'date': 'Дата',
        }
        help_texts = {
            'title': 'Введите заголовок новости',
            'content': 'Введите текст новости',
            'date': 'Введите дату новости',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст новости'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Выберите дату'}),
        }