from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import UserListAndRegistrationSerializer, GetTokenSerializer
from users.models import User


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListAndRegistrationSerializer


@api_view(['POST'])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    password = serializer.validated_data.get('password')
    email = serializer.validated_data.get('email')
    user = get_object_or_404(User, email=email)
    auth = authenticate(username=user.username, password=password)
    if auth:
        jwt_token = AccessToken.for_user(user)
        return Response(
            f'Access Token: {str(jwt_token)}',
            status=status.HTTP_200_OK
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
