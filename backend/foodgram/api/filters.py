from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag

User = get_user_model()


class CustomSearchFilter(SearchFilter):
    """Кастомный класс поиска.

    Переопределил параметр запроса.
    """
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    """Кастомный класс фильтра для рецептов.

    Поиск по полям:
        author - выбор рецепта только от конкретного пользователя
        tags - выбор рецептов только с определенным тегом
        is_favorited - выбор рецептов только из раздела Избранное
        is_in_shopping_cart - выбор рецептов только из раздела Список покупок
    """
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def filter_is_favorited(self, queryset, name, value):
        """Фильтр по полю is_favorited (в избранном у текущего пользователя).

        Returns:
            queryset: Для пользователей возвращает рецепты, которые
            находятся в избранном у текущего пользователя. Для гостей 
            возвращает все рецепты.
        """
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """Фильтр по полю is_in_shopping_cart (в списке покупок у текущего 
        пользователя).

        Returns:
            queryset: Для пользователей возвращает рецепты, которые
            находятся в списке покупок у текущего пользователя. Для гостей 
            возвращает все рецепты.
        """
        if value and not self.request.user.is_anonymous:
            return queryset.filter(shopping_carts__user=self.request.user)
        return queryset
