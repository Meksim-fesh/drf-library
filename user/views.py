from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserManageSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """Register a new user with email and password"""
        return super().post(request, *args, **kwargs)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserManageSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        """Returns detail info about authenticated user"""
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Updates info about authenticated user
        (requires all fields to be provided)
        """
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Updates info about authenticated user
        (does not require all fields to be provided)
        """
        return super().patch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
