from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from book.models import Book
from book.serializers import BookListSerializer, BookSerializer


BOOK_LIST_URL = reverse("book:book-list")


def sample_book(**params) -> Book:
    payload = {
        "title": "Test Title",
        "author": "Test Author",
        "cover": "Hard",
        "inventory": 10,
        "daily_fee": 20.99,
    }
    payload.update(params)
    return Book.objects.create(**payload)


class BookTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        user = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="password",
        )
        self.client.force_authenticate(user)

    def test_list_book(self):
        sample_book()
        sample_book()
        sample_book()

        response = self.client.get(BOOK_LIST_URL)

        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        payload = {
            "title": "Test_title",
            "author": "Test_author",
            "cover": "Soft",
            "inventory": 50,
            "daily_fee": 10.99,
        }

        response = self.client.post(
            BOOK_LIST_URL,
            payload
        )

        book = Book.objects.first()
        serializer = BookSerializer(book)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
