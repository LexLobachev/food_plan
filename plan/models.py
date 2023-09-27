from django.db import models


class MenuType(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Тип меню'
        verbose_name_plural = 'Типы меню'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    calories = models.FloatField('Калорийность на 100г')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.title


class IngredientItem(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='items', on_delete=models.PROTECT)
    quantity = models.FloatField('Кол-во (в граммах).', default=100)
    recipe = models.ForeignKey('Recipe', verbose_name='В рецепте', related_name='ingredients', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Ингредиент в заказе'
        verbose_name_plural = 'Ингредиенты в заказе'

    def __str__(self):
        return f'{self.ingredient.title}: {self.quantity} г.'


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField('Описание рецепта')
    text = models.TextField('Текст рецепта')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(verbose_name='Описание подписки')

    # TODO: user = models.ForeignKey('User')

    type = models.ForeignKey(MenuType, related_name='subscriptions', on_delete=models.PROTECT)

    expire_date = models.DateField(verbose_name='Дата окончания подписки')

    have_breakfast = models.BooleanField('Завтраки', default=False)
    have_dinner = models.BooleanField('Обеды', default=False)
    have_supper = models.BooleanField('Ужины', default=False)
    have_dessert = models.BooleanField('Десерты', default=False)

    number_of_persons = models.PositiveIntegerField('Кол-во персон', default=1)

    allergies = models.ManyToManyField(Ingredient, related_name='banned_for_subscriptions', verbose_name='Ингредиенты с аллергией')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.title} - self.user.name(TODO)'
