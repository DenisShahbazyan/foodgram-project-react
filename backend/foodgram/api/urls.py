from django.urls import path

from .views import UserList, get_token

app_name = 'api'

urlpatterns = [
    path('users/', UserList.as_view()),
    path('auth/token/login/', get_token, name='get_token'),
]
