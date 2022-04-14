from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import mixins, viewsets

from recipes.models import Ingredient, Recipe, Subscription, Tag

from .serializers import (CreateUpdateDestroyRecipeSerializer,
                          IngredientSerializer, ListRetrieveRecipeSerializer,
                          SubscribeSerializer, SubscriptionSerializer,
                          TagSerializer)

User = get_user_model()


class UserViewSet(UserViewSet):
    queryset = User.objects.all()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = ListRetrieveRecipeSerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ListRetrieveRecipeSerializer
        return CreateUpdateDestroyRecipeSerializer


class SubscriptionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(followings__user=user)
        return queryset


class SubscribeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
