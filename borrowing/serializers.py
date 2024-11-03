from datetime import date

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

    def validate(self, attrs):
        book = attrs["book"]
        if book.inventory <= 0:
            raise serializers.ValidationError(
                "There are no more books left, try again later"
            )
        book.inventory = book.inventory - 1
        book.save()
        return attrs


class BorrowingReturnSerializer(BorrowingSerializer):
    class Meta:
        model = Borrowing
        fields = []

    def update(self, instance, validated_data):
        actual_return_date = instance.actual_return_date
        if actual_return_date:
            raise serializers.ValidationError(
                "The borrowing has already been returned"
            )

        book = instance.book
        book.inventory = book.inventory + 1
        book.save()

        actual_return_date = date.today()
        validated_data["actual_return_date"] = actual_return_date

        return super().update(instance, validated_data)
