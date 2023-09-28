from django import forms
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

from plan.forms import CustomAuthenticationForm


def index(request):
    """
    View function for home page of site.
    """
    return render(request, "index.html")


def lk(request):
    context = {'client': {'name': 'Alex', 'mail': 'alex@mail.ru', 'password': 'qwerty'}}
    # context = {'client': Client.objects.get(id=id)}
    return render(request, 'lk.html', context=context)


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


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "registration/login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")

        return render(request, "registration/login.html", context={
            'form': form,
            'ivalid': True,
        })


def register(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/registration.html', {'form': form})
