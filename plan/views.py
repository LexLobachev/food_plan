import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from plan.forms import CustomAuthenticationForm, Login, ImageForm
from plan.models import Recipe, StartRecipe, Subscription, Avatar


def index(request):
    """
    View function for home page of site.
    """
    return render(request, "index.html")


def update_profile(request, user):
    if request.GET['NAME'] and request.GET['EMAIL']:
        user.first_name = request.GET['NAME']
        user.email = request.GET['EMAIL']
        user.save()
    elif request.GET['NAME'] and not request.GET['EMAIL']:
        user.first_name = request.GET['NAME']
        user.save()
    elif not request.GET['NAME'] and request.GET['EMAIL']:
        user.email = request.GET['EMAIL']
        user.save()
    return user


@login_required(login_url='/login/')
def lk(request):
    form = ImageForm()
    recipe = list(Recipe.objects.all())
    user = request.user
    if request.GET:
        print('GET', request.GET)
        update_profile(request, user)

    if request.method == 'FILES':
        a =Avatar.objects.update_or_create(user=user, defaults={
            'image': request.FILES['image']
        })
        a.save()
    try:
        start_recipe = StartRecipe.objects.get(user=user)
    except StartRecipe.DoesNotExist:
        start_recipe = None
    if not start_recipe:
        recipes = StartRecipe.objects.create(user=user)
        for i in range(3):
            random_recipe = random.choice(recipe)
            recipes.recipe.add(random_recipe)
        start_recipe = StartRecipe.objects.filter(user=user)[0]
    subscriptions = list(Subscription.objects.filter(user=user))
    if subscriptions:
        for subscription in subscriptions:
            if subscription.start_date >= subscription.expire_date:
                subscription.is_acive = False
                subscription.save()
    if not Avatar.objects.filter(user=user):
        Avatar.objects.create(user=user)
    avatar = Avatar.objects.get(user=user)
    context = {
        'user': user,
        'start_recipe': start_recipe,
        'subscriptions': subscriptions,
        'avatar': avatar,
        'form': form,
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
