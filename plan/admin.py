from django.contrib import admin

from .models import (Subscription, MenuType,
                     Ingredient, IngredientItem, Recipe, StartRecipe, Avatar, CategoryIngredient)


class IngredientItemInline(admin.TabularInline):
    model = IngredientItem
    extra = 0


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
    list_display = ['id', 'title', 'menu_type', 'image', 'description', 'text', 'thumbnail_preview']
    inlines = [
        IngredientItemInline
    ]
    readonly_fields = ['thumbnail_preview']

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True


@admin.register(StartRecipe)
class StartRecipeAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'image']


@admin.register(CategoryIngredient)
class CategoryIngredientAdmin(admin.ModelAdmin):
    pass
