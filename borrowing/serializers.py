from rest_framework import serializers

from book.serializers import BookListSerializer, BookSerializer
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingListSerializer(BorrowingSerializer):
    book = BookListSerializer(read_only=True)
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)


class BorrowingDetailSerializer(BorrowingListSerializer):
    book = BookSerializer(read_only=True)


class BorrowingCreateSerializer(BorrowingSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "book",
            "user",
        )
        read_only_fields = ("borrow_date", "user")
