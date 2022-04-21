from django.contrib import admin

from .models import (AmountIngredientForRecipe, Favorite, Ingredient, Recipe,
                     ShoppingCart, Tag)


class IngredientInline(admin.TabularInline):
    model = AmountIngredientForRecipe
    extra = 1


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_editable = ('user', 'recipe')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_editable = ('user', 'recipe')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ('author', 'name', 'image', 'text', 'cooking_time', 'tags')
    list_display = (
        'id', 'author', 'name', 'image', 'text', 'cooking_time', 'get_cout'
    )
    filter_horizontal = ('tags',)
    list_filter = ('author', 'name')
    list_editable = ('author', 'name', 'image', 'text', 'cooking_time')
    inlines = (IngredientInline,)

    def get_cout(self, obj):
        return obj.favorites.count()

    get_cout.short_description = 'Кол-во добавления в избранное'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    list_editable = ('name', 'measurement_unit')
    search_fields = ('id', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')
