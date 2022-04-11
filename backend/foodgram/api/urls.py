from django.urls import include, path
from rest_framework import routers

from .views import (UserViewSet, get_token, TagViewSet,
                    IngredientViewSet, RecipeViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', get_token, name='get_token'),
    path('auth/', include('djoser.urls.authtoken')),
]
