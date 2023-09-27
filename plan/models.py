from django.db import models

# Create your models here.


class MenuType(models.Model):
    title = models.CharField(max_length=200)


class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    calories = models.FloatField('Калорийность на 100г')


class IngredientItem(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='items', on_delete=models.PROTECT)
    quantity = models.FloatField('Кол-во (в граммах).', default=100)
    recipe = models.ForeignKey('Recipe', verbose_name='В рецепте', related_name='ingredients', on_delete=models.PROTECT)


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField('Описание рецепта')
    text = models.TextField('Текст рецепта')


class Subscription(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(verbose_name='Описание подписки')

    type = models.ForeignKey(MenuType, related_name='subscriptions', on_delete=models.PROTECT)

    expire_date = models.DateField(verbose_name='Дата окончания подписки')

    have_breakfast = models.BooleanField('Завтраки', default=False)
    have_dinner = models.BooleanField('Обеды', default=False)
    have_supper = models.BooleanField('Ужины', default=False)
    have_dessert = models.BooleanField('Десерты', default=False)

    number_of_persons = models.PositiveIntegerField('Кол-во персон', default=1)

    allergies = models.ManyToManyField(Ingredient, related_name='banned_for_subscriptions', verbose_name='Ингредиенты с аллергией')
