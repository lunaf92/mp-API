from rest_framework import generics
from .serializers import UserSerializer, AuthUserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthUserSerializer
    renderer_class = api_settings.DEFAULT_RENDERER_CLASSES
