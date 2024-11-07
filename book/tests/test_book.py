from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from book.models import Book
from book.serializers import BookListSerializer, BookSerializer


BOOK_LIST_URL = reverse("book:book-list")


def get_book_detail_url(book_id: int):
    return reverse("book:book-detail", args=[book_id])


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

    def test_retrieve_book(self):
        book = sample_book()
        serializer = BookSerializer(book)

        response = self.client.get(
            get_book_detail_url(book.id)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put_book(self):
        new_title = "New Test Title"
        old_title = "Old Test Title"

        book = sample_book(title=old_title)

        payload = {
            "title": new_title,
            "author": "Test Author",
            "cover": "Hard",
            "inventory": 10,
            "daily_fee": 20.99,
        }

        response = self.client.put(
            get_book_detail_url(book.id),
            payload,
        )

        book.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(book.title, new_title)

    def test_patch_book(self):
        new_title = "New Test Title"
        old_title = "Old Test Title"

        book = sample_book(title=old_title)

        payload = {
            "title": new_title,
        }

        response = self.client.patch(
            get_book_detail_url(book.id),
            payload,
        )

        book.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(book.title, new_title)

    def test_delete_book(self):
        book = sample_book()
        books_amount = Book.objects.count()

        self.assertEqual(books_amount, 1)

        response = self.client.delete(
            get_book_detail_url(book.id)
        )

        books_amount = Book.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(books_amount, 0)
