from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from user.serializers import UserManageSerializer, UserSerializer


REGISTER_USER_URL = reverse("user:user-create")
MANAGE_USER_URL = reverse("user:user-manage")


class UnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_new_user(self):
        payload = {
            "email": "user@test.com",
            "password": "password",
        }

        response = self.client.post(REGISTER_USER_URL, payload)

        user = get_user_model().objects.first()
        serializer = UserSerializer(user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)


class AuthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="password",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_user(self):
        user = self.user
        serializer = UserManageSerializer(user)

        response = self.client.get(MANAGE_USER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(serializer.data)
        self.assertEqual(response.data, serializer.data)

    def test_put_user(self):
        first_name = "Admin"
        last_name = "Test"

        payload = {
            "email": "admin@test.com",
            "first_name": first_name,
            "last_name": last_name,
            "password": "password",
        }

        response = self.client.put(
            MANAGE_USER_URL, payload,
        )

        user = get_user_model().objects.first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)

    def test_patch_user(self):
        first_name = "New Name"

        payload = {
            "first_name": first_name,
        }

        response = self.client.patch(
            MANAGE_USER_URL, payload,
        )

        user = get_user_model().objects.first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.first_name, first_name)
