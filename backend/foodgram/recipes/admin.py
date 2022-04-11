from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, ShoppingCart, Subscription,
                     Tag, AmountIngredientForRecipe)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    filter_horizontal = ('recipe',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    filter_horizontal = ('recipe',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    list_editable = ('user', 'author')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'image', 'text', 'cooking_time')
    filter_horizontal = ('tags', 'ingredients')
    list_filter = ('author', 'name')
    list_editable = ('author', 'name', 'image', 'text', 'cooking_time')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    list_editable = ('name', 'measurement_unit')


@admin.register(AmountIngredientForRecipe)
class AmountIngredientForRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')
