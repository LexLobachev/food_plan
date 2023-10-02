from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe


class MenuType(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True,  blank=True, null=True)

    class Meta:
        verbose_name = 'Тип меню'
        verbose_name_plural = 'Типы меню'

    def __str__(self):
        return f'{self.pk} {self.title}'


class CategoryIngredient(models.Model):
    title = models.CharField('Категория', max_length=200)

    class Meta:
        verbose_name = 'Категория ингредиента'
        verbose_name_plural = 'Категории ингредиентов'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField('Ингредиент', max_length=200)
    calories = models.FloatField('Калорийность на 100г')
    category = models.ForeignKey(CategoryIngredient, related_name='ingredients',
                                 on_delete=models.PROTECT, blank=True, null=True)

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
    menu_type = models.ForeignKey(MenuType, verbose_name='Тип меню', related_name='recipes', on_delete=models.PROTECT)
    image = models.ImageField('Изображение', upload_to='recipes/')
    description = models.TextField('Описание рецепта')
    text = models.TextField('Текст рецепта')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title

    @property
    def thumbnail_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="200" height="200" />'.format(self.image.url))
        return ""


class StartRecipe(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='start_recipes',
                             on_delete=models.PROTECT, blank=True, null=True)
    recipe = models.ManyToManyField(Recipe, verbose_name='Рецепт', related_name='start_recipes', blank=True)

    class Meta:
        verbose_name = 'Стартовый рецепт'
        verbose_name_plural = 'Стартовые рецепты'

    def __str__(self):
        return f'{self.user.first_name} рецепт {self.recipe}'


class Subscription(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(verbose_name='Описание подписки')

    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='subscriptions', on_delete=models.PROTECT)

    type = models.ForeignKey(MenuType, related_name='subscriptions', on_delete=models.PROTECT)

    start_date = models.DateField(verbose_name='Дата начала подписки', default=timezone.now)
    expire_date = models.DateField(verbose_name='Дата окончания подписки')

    have_breakfast = models.BooleanField('Завтраки', default=False)
    have_dinner = models.BooleanField('Обеды', default=False)
    have_supper = models.BooleanField('Ужины', default=False)
    have_dessert = models.BooleanField('Десерты', default=False)

    number_of_persons = models.PositiveIntegerField('Кол-во персон', default=1)

    allergies = models.ManyToManyField(CategoryIngredient, related_name='banned_for_subscriptions',
                                       verbose_name='Ингредиенты с аллергией', blank=True)
    is_acive = models.BooleanField('Активная', default=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.title} - {self.user.first_name}'


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', verbose_name='Аватар', default='avatars/default.jpeg')

    def __str__(self):
        return f'{self.user.first_name} - {self.image.name}'


