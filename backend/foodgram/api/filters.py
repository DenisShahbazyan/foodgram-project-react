from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag

User = get_user_model()


class CustomSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
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
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(shopping_carts__user=self.request.user)
        return queryset
