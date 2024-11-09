from datetime import date, timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from book.models import Book
from borrowing.models import Borrowing, Payment
from borrowing.serializers import (
    PaymentDetailSerializer,
    PaymentListSerializer

)


PAYMENT_LIST_URL = reverse("borrowing:payment-list")


def get_detail_url(payment_id: int, path: str = "borrowing:payment-detail"):
    return reverse(path, args=[payment_id,])


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


def sample_payment(borrowing: Borrowing, **params) -> Payment:
    payload = {
        "status": "Pending",
        "type": "Payment",
        "borrowing": borrowing,
        "session_url": "https://www.example.com/",
        "session_id": "qwertyuiop",
        "money_to_pay": 20.99
    }
    payload.update(**params)
    return Payment.objects.create(**payload)


class PaymentTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="password",
        )
        self.client.force_authenticate(self.user)

    def test_list_payment(self):
        user = self.user
        book = sample_book()
        borrowing = sample_borrowing(user, book)

        sample_payment(borrowing)
        sample_payment(borrowing)
        sample_payment(borrowing)

        payments = Payment.objects.all()
        serializer = PaymentListSerializer(payments, many=True)

        response = self.client.get(PAYMENT_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_payment(self):
        user = self.user
        book = sample_book()
        borrowing = sample_borrowing(user, book)
        payment = sample_payment(borrowing)

        serializer = PaymentDetailSerializer(payment)

        response = self.client.get(get_detail_url(payment.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_success_page_change_payment_status(self):
        user = self.user
        book = sample_book()
        borrowing = sample_borrowing(user, book)
        payment = sample_payment(borrowing)

        self.assertEqual(payment.status, "Pending")

        response = self.client.patch(
            get_detail_url(payment.id, "borrowing:payment-success")
        )

        payment.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Success")
        self.assertEqual(payment.status, "Paid")

    def test_cancel_page_do_not_change_payment_status(self):
        user = self.user
        book = sample_book()
        borrowing = sample_borrowing(user, book)
        payment = sample_payment(borrowing)

        self.assertEqual(payment.status, "Pending")

        response = self.client.get(
            get_detail_url(payment.id, "borrowing:payment-cancel")
        )

        payment.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data,
            "Payment was canceld. You can try to pay again within 24 hours."
        )
        self.assertEqual(payment.status, "Pending")
