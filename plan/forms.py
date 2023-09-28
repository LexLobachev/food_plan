from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomAuthenticationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(
        attrs={
            'class': 'form-control', 'placeholder': 'Введите своё имя',
            'type': 'text', 'id': 'name'
        })
    )
    username = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={
            'class': 'form-control', 'placeholder': 'Введите свой Email',
            'type': 'email', 'id': 'email', 'aria - describedby': 'emailHelp',
        }
    ))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control', 'placeholder': 'Пароль',
            'id': 'password', 'type': 'password',
               }
    ))
    password2 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control  cake__textinput', 'placeholder': 'Пароль',
            'id': 'PasswordConfirm', 'type': 'password'
        }
    ))

    class Meta:
        model = User
        fields = ('first_name', 'username', 'password1', 'password2')

