from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Login(forms.Form):
    username = forms.EmailField(
        label='Email', max_length=95, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': 'Введите свой Email',
            'aria - describedby': 'emailHelp',
            'type': 'email',
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=95, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'id': 'password',
            'type': 'password',
        })
    )


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

