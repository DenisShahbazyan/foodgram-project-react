from django.urls import include, path
from rest_framework import routers

from .views import (IngredientViewSet, RecipeViewSet, SubscribeViewSet,
                    SubscriptionViewSet, TagViewSet, UserViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register('users/subscriptions',
                SubscriptionViewSet,
                basename='subscription')
router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
router.register(r'users/(?P<author_id>[\d]+)/subscribe',
                SubscribeViewSet,
                basename='subscribe',)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
