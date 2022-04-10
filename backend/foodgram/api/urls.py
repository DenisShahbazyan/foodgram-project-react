from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, get_token

app_name = 'api'

router = routers.DefaultRouter()

router.register('users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', get_token, name='get_token'),
]
