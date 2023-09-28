from django.contrib import admin

from .models import Subscription, MenuType
from .models import Ingredient, IngredientItem, Recipe


@admin.register(MenuType)
class MenuTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(IngredientItem)
class IngredientItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass

