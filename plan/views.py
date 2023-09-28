import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from plan.forms import CustomAuthenticationForm, Login
from plan.models import Recipe, StartRecipe


def index(request):
    """
    View function for home page of site.
    """
    return render(request, "index.html")


@login_required(login_url='/login/')
def lk(request):
    if request.GET:
        print('GET', request.GET)
    recipe = list(Recipe.objects.all())
    user = request.user
    start_recipe = StartRecipe.objects.filter(user=user)[0]
    if not start_recipe:
        recipes = StartRecipe.objects.create(user=user)
        for i in range(3):
            random_recipe = random.choice(recipe)
            recipes.recipe.add(random_recipe)
        start_recipe = StartRecipe.objects.filter(user=user)[0]
    context = {
        'user': user,
        'start_recipe': start_recipe,
    }
    return render(request, 'lk.html', context=context)


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
            username = form.cleaned_data.get('username')
            User.objects.update_or_create(username=username, defaults={'email': username})
            return redirect('/login/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/registration.html', {'form': form})


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    context = {
        'recipe': recipe,
    }

    return render(request, 'card1.html', context)