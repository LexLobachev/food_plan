from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from plan.models import Avatar, MenuType


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


class ImageForm(forms.Form):
    image = forms.FileField(label='Выберите изображение', widget=forms.FileInput(
        attrs={
            'class': 'form-control', 'placeholder': 'Выберите изображение',
            'type': 'file', 'id': 'file', 'aria - describedby': 'fileHelp',
            'name': 'file'
        }
    ))


SUBS_PERIOD = (
    ('1', 1),
    ('3', 3),
    ('6', 6),
    ('12', 12),
)

PERS_QUANTITY = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
)

MENU_TYPE = ((menu_type.id, menu_type.title) for menu_type in MenuType.objects.all())

ALLERGENS = (
    ('fish', 'Рыба и морепродукты'),
    ('meat', 'Мясо'),
    ('cereals', 'Зерновые'),
    ('honey', 'Продукты пчеловодства'),
    ('nuts', 'Орехи и бобовые'),
    ('milk', 'Молочные продукты'),
)

MEAL_TYPE = (
    ('breakfast', 'Завтрак'),
    ('lunch', 'Обед'),
    ('dinner', 'Ужин'),
    ('dessert', 'Десерт'),
)


class OrderForm(forms.Form):
    promo_code = forms.CharField(label='Промокод', required=False)
    subscription_period = forms.ChoiceField(label='Срок подписки', choices=SUBS_PERIOD, required=True)
    persons_quantity = forms.ChoiceField(label='Количество персон', choices=PERS_QUANTITY,  required=True)
    meals = forms.MultipleChoiceField(label='Прием пищи', choices=MEAL_TYPE,  required=True)
    menu_type = forms.ChoiceField(label='Тип меню', choices=MENU_TYPE, required=True)
    allergens = forms.ChoiceField(label='Аллергии', choices=ALLERGENS, required=False)
