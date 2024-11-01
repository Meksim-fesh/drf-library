from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserManageSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserManageSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get_object(self):
        return self.request.user
