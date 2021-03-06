from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser import views as djoser_views
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .filters import CustomSearchFilter, RecipeFilter
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrIsAdminOrReadOnly
from .serializers import (CreateUpdateDestroyRecipeSerializer,
                          IngredientSerializer, ListRetrieveRecipeSerializer,
                          SimpleRecipeSerializer, SubscriptionSerializer,
                          TagSerializer)

User = get_user_model()


class UserViewSet(djoser_views.UserViewSet):
    queryset = User.objects.all()
    pagination_class = CustomPageNumberPagination

    @action(detail=True, methods=('post',), url_path='subscribe',
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response(
                {'errors': 'Вы не можете подписываться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.subscribe.filter(id=author.id).exists():
            return Response(
                {'errors': 'Вы уже подписаны на данного пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.subscribe.add(author)
        serializer = SubscriptionSerializer(
            author, data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                {'errors': 'Вы не можете отписываться от самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if author:
            user.subscribe.remove(author)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'errors': 'Вы уже отписались'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=('get',), url_path='subscriptions',
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        queryset = user.subscribe.all()
        pagination = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pagination,
            data=list(request.data),
            many=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (CustomSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrIsAdminOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ListRetrieveRecipeSerializer
        return CreateUpdateDestroyRecipeSerializer

    @action(detail=True, methods=('post',), url_path='favorite',
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        _, created = Favorite.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if not created:
            return Response(
                {'errors': 'Рецепт уже добавлен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SimpleRecipeSerializer(recipe, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def del_favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        obj = Favorite.objects.filter(user=request.user, recipe=recipe)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт уже удален'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=('post',), url_path='shopping_cart',
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        _, created = ShoppingCart.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if not created:
            return Response(
                {'errors': 'Рецепт уже добавлен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SimpleRecipeSerializer(recipe, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def del_shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        obj = ShoppingCart.objects.filter(user=request.user, recipe=recipe)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт уже удален'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=('get',), url_path='download_shopping_cart',
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        carts = ShoppingCart.objects.filter(user=request.user)
        tmp = {}
        for cart in carts:
            items = cart.recipe.amountingredientforrecipes.all()
            for item in items:
                ingredient = item.ingredient.name
                amount = item.amount
                measurement_unit = item.ingredient.measurement_unit
                if f'{ingredient}|{measurement_unit}' not in tmp:
                    tmp[f'{ingredient}|{measurement_unit}'] = {
                        'amount': amount
                    }
                else:
                    tmp[f'{ingredient}|{measurement_unit}']['amount'] = (
                        tmp[f'{ingredient}|{measurement_unit}']['amount']
                        + amount
                    )

        shopping_list = []
        for item in tmp:
            ingredient = item.split('|')[0]
            amount = tmp[item]["amount"]
            measurement_unit = item.split('|')[1]
            shopping_list.append(
                f'{ingredient} - {amount}, {measurement_unit}\n'
            )
        response = HttpResponse(shopping_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = (
            'attachment;' 'filename="shopping_list.txt"'
        )
        return response
