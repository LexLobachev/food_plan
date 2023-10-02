import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from plan.forms import CustomAuthenticationForm, Login, ImageForm
from plan.models import Recipe, StartRecipe, Subscription, Avatar, CategoryIngredient
from plan.operations import create_subscription
from food_plan.settings import YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY, WEBSITE_URL
from plan.forms import CustomAuthenticationForm, Login, ImageForm, OrderForm
from plan.models import Recipe, StartRecipe, Subscription, Avatar

from yookassa import Payment, Configuration


def index(request):
    """
    View function for home page of site.
    """
    return render(request, "index.html")


@login_required(login_url='/login/')
def view_random_recipe(request):
    """
    View function for random card recipe of site.
    """
    user = request.user
    start_recipe = StartRecipe.objects.get(user=user)
    recipe = random.choice(start_recipe.recipe.all())
    ingredients = recipe.ingredients.all()
    context = {
        'recipe': recipe,
        'ingredients': ingredients
    }

    return render(request, "card2.html", context)


def card3(request):
    """
    View function for home page of site.
    """
    return render(request, "card3.html")


def order(request):
    """
    View function for order page of site.
    """
    if request.method == 'POST':
        subscription = []
        for key in request.POST:
            subscription.append({'key': key, 'value': request.POST[key]})
        print(subscription)
        subscription, created = create_subscription(subscription, request)

    allergies = list(CategoryIngredient.objects.all())
    context = []
    for allergy in allergies:
        context.append({'title': allergy.title, 'id': allergy.id})
    return render(request, 'order.html', context={'allergies': context})
    # if request.method == 'POST':
    #     form = OrderForm(request.POST)
    #     if form.is_valid():
    #         Configuration.account_id = YOOKASSA_SHOP_ID
    #         Configuration.secret_key = YOOKASSA_SECRET_KEY
    #
    #         print(form.cleaned_data)
    #         promo_code = form.cleaned_data['promo_code']
    #         subscription_period = form.cleaned_data['subscription_period']
    #         persons_quantity = form.cleaned_data['persons_quantity']
    #         meals = form.cleaned_data['meals']
    #         menu_type = form.cleaned_data['menu_type']
    #         allergens = form.cleaned_data['allergens']
    #
    #         subscription = Subscription.objects.create(
    #             user=request.user,
    #             expire_date=datetime.now() + timedelta(days=subscription_period * 30),
    #             number_of_persons=persons_quantity,
    #             type=menu_type,
    #             allergies=allergens
    #         )
    #
    #         payment = Payment.create({
    #             "amount": {
    #                 "value": 20,
    #                 "currency": "RUB"
    #             },
    #             "confirmation": {
    #                 "type": "redirect",
    #                 "return_url": f'{WEBSITE_URL}/payment_result/?subscription_id={subscription.id}'
    #             },
    #             "capture": True,
    #             "description": None
    #         })
    #
    #         return redirect(payment.confirmation.confirmation_url)
    # else:
    #     form = OrderForm()
    # return render(request, 'order.html', {'form': form})


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
        while True:
            random_recipe = random.choice(recipe)
            recipes.recipe.add(random_recipe)
            if recipes.recipe.count() == 3:
                break
        recipes.save()
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
    ingredients = recipe.ingredients.all()
    context = {
        'recipe': recipe,
        'ingredients': ingredients
    }

    return render(request, 'card2.html', context)
