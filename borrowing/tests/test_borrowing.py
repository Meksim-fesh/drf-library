from datetime import date, timedelta
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from book.models import Book
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
    BorrowingListSerializer
)


BORROWING_LIST_URL = reverse("borrowing:borrowing-list")


def get_detail_url(borrow_id: int):
    return reverse("borrowing:borrowing-detail", args=[borrow_id,])


def generate_expected_return_date(amount_of_days: int = 5) -> date:
    return date.today() + timedelta(days=amount_of_days)


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


def sample_borrowing(user, book: Book, **params) -> Borrowing:
    payload = {
        "expected_return_date": generate_expected_return_date(),
        "book": book,
        "user": user,
    }
    payload.update(**params)
    return Borrowing.objects.create(**payload)


class BorrowingTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="password",
        )
        self.client.force_authenticate(self.user)

    def test_list_borrowing(self):
        user = self.user
        book = sample_book()

        sample_borrowing(user, book)
        sample_borrowing(user, book)
        sample_borrowing(user, book)

        borrowings = Borrowing.objects.all()
        serializer = BorrowingListSerializer(borrowings, many=True)

        response = self.client.get(BORROWING_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    @patch("borrowing.serializers.BorrowingCreateSerializer.get_checkout_url")
    @patch(
        "borrowing.serializers.BorrowingCreateSerializer.send_notification"
    )
    def test_create_borrowing_call_send_notification(
        self,
        mocked_notification,
        mocked_session,
    ):
        mocked_session.return_value = "https://checkout.stripe.com/"
        user = self.user
        book = sample_book()

        payload = {
            "expected_return_date": generate_expected_return_date(),
            "book": book.id,
            "user": user.id,
        }

        response = self.client.post(
            BORROWING_LIST_URL,
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(mocked_notification.called)

    @patch("borrowing.serializers.BorrowingCreateSerializer.get_checkout_url")
    @patch(
        "borrowing.serializers.BorrowingCreateSerializer.send_notification"
    )
    def test_create_borrowing_call_create_checkout_stripe_session(
        self,
        mocked_notification,
        mocked_session,
    ):
        mocked_session.return_value = "https://checkout.stripe.com/"
        user = self.user
        book = sample_book()

        payload = {
            "expected_return_date": generate_expected_return_date(),
            "book": book.id,
            "user": user.id,
        }

        response = self.client.post(
            BORROWING_LIST_URL,
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(mocked_session.called)

    @patch("borrowing.serializers.BorrowingCreateSerializer.get_checkout_url")
    @patch(
        "borrowing.serializers.BorrowingCreateSerializer.send_notification"
    )
    def test_create_borrowing(
        self,
        mocked_notification,
        mocked_session,
    ):
        mocked_session.return_value = "https://checkout.stripe.com/"
        user = self.user
        book = sample_book()

        payload = {
            "expected_return_date": generate_expected_return_date(),
            "book": book.id,
            "user": user.id,
        }

        response = self.client.post(
            BORROWING_LIST_URL,
            payload,
        )

        borrowing = Borrowing.objects.first()
        serializer = BorrowingCreateSerializer(borrowing)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_borrowing(self):
        user = self.user
        book = sample_book()
        borrowing = sample_borrowing(user, book)

        response = self.client.get(get_detail_url(borrowing.id))

        serializer = BorrowingDetailSerializer(borrowing)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put_borrowing(self):
        user = self.user
        book = sample_book()
        old_expected_date = generate_expected_return_date(2)
        new_expected_date = generate_expected_return_date(8)

        borrowing = sample_borrowing(
            user,
            book,
            expected_return_date=old_expected_date
        )

        payload = {
            "borrow_date": date.today(),
            "expected_return_date": new_expected_date,
            "book": book.id,
            "user": user.id,
        }

        response = self.client.put(
            get_detail_url(borrowing.id),
            payload,
        )

        borrowing.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(borrowing.expected_return_date, new_expected_date)

    def test_patch_borrowing(self):
        user = self.user
        book = sample_book()
        old_expected_date = generate_expected_return_date(2)
        new_expected_date = generate_expected_return_date(8)

        borrowing = sample_borrowing(
            user,
            book,
            expected_return_date=old_expected_date
        )

        payload = {
            "expected_return_date": new_expected_date
        }

        response = self.client.patch(
            get_detail_url(borrowing.id),
            payload,
        )

        borrowing.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(borrowing.expected_return_date, new_expected_date)
