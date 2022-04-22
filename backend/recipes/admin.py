from django.contrib import admin
from django.utils.safestring import mark_safe

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
        'id', 'author', 'name', 'get_image', 'text', 'cooking_time', 'get_cout'
    )
    read_only_fields = ('get_image',)
    filter_horizontal = ('tags',)
    list_filter = ('author', 'name')
    list_editable = ('author', 'name', 'text', 'cooking_time')
    inlines = (IngredientInline,)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30"')

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
