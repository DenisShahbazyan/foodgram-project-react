from django.contrib.auth import authenticate
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users.models import User
from .serializers import (GetTokenSerializer, UserSerializer,
                          UserSetPasswordSerializer, TagSerializer,
                          IngredientSerializer, RecipeSerializer)
from recipes.models import Tag, Ingredient, Recipe


class ListCreateRetrieveViewSet(mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet
                                ):
    pass


class UserViewSet(ListCreateRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=('get',), url_path='me',
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',), url_path='set_password',
            permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        serializer = UserSetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        new_password = serializer.validated_data.get('new_password')
        current_password = serializer.validated_data.get('current_password')
        auth = authenticate(username=user, password=current_password)
        if auth:
            user.set_password(new_password)
            user.save()
            return Response(
                serializer.data,
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    password = serializer.validated_data.get('password')
    email = serializer.validated_data.get('email')
    user = get_object_or_404(User, email=email)
    auth = authenticate(username=user, password=password)
    if auth:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'auth_token': str(token)},
            status=status.HTTP_200_OK
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
