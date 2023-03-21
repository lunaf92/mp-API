from rest_framework import generics, authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, AuthUserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthUserSerializer
    renderer_class = api_settings.DEFAULT_RENDERER_CLASSES

class RetrieveUpdateSelfView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    
    
    def get_object(self):
        return self.request.user
    