from django.shortcuts import get_object_or_404
from datetime import date
from dateutil.relativedelta import relativedelta

from plan.models import Subscription, MenuType, CategoryIngredient


def create_subscription(subscription, request):
    cost_per_month = 100
    user = request.user
    terms = {
        '0': 1,
        '1': 3,
        '2': 6,
        '3': 12,
    }
    menu = None
    breakfast = False
    lunch = False
    dinner = False
    dessert = False
    persons = 1
    term = None
    allergies = []
    description = ''
    print(subscription)
    for item in subscription:
        key = item['key']
        if key == 'month':
            term = terms.get(item['value'])
            description = f'Subscription for {term} months'
        elif key == 'select1' and item['value'] == '0':
            breakfast = True
            description += ', breakfast'
        elif key == 'select2' and item['value'] == '0':
            lunch = True
            description += ', lunch'
        elif key == 'select3' and item['value'] == '0':
            dinner = True
            description += ', dinner'
        elif key == 'select4' and item['value'] == '0':
            dessert = True
            description += ', dessert'
        elif key == 'select5':
            persons = int(item['value']) + 1
            description += f' for {persons} persons'
        elif 'allergy_' in key:
            allergy_id = int(key.split('_')[1])
            print(allergy_id,  item['value'])
            allergies.append(get_object_or_404(CategoryIngredient, pk=allergy_id))
        elif key == 'foodtype':
            if item['value'] == 'keto':
                menu = get_object_or_404(MenuType, slug='keto')
            elif item['value'] == 'veg':
                menu = get_object_or_404(MenuType, slug='veg')
            elif item['value'] == 'low':
                menu = get_object_or_404(MenuType, slug='low')
            elif item['value'] == 'classic':
                menu = get_object_or_404(MenuType, slug='classic')

    print('allergies = ', allergies)

    subscriptions, created = Subscription.objects.get_or_create(
        title=f'Subscription for {term} months',
        description=description,
        have_breakfast=breakfast,
        have_dinner=lunch,
        have_supper=dinner,
        have_dessert=dessert,
        number_of_persons=persons,
        expire_date=date.today() + relativedelta(months=+term),
        # allergies=,
        user=user,
        type=menu
    )
    for allergie in allergies:
        subscriptions.allergies.add(allergie)
    subscriptions.save()
    return subscriptions, created
