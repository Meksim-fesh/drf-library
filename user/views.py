from rest_framework import generics

from user.serializers import UserManageSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserManageSerializer

    def get_object(self):
        return self.request.user
