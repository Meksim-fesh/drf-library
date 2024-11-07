from datetime import date

from rest_framework import serializers

from book.serializers import BookListSerializer, BookSerializer
from borrowing.models import Borrowing, Payment
from borrowing.stripe_payment import create_checkout_session
from borrowing.telegram import send_notification


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


class PaymentBorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "session_url",
            "session_id",
            "money_to_pay",
        ]


class BorrowingDetailSerializer(BorrowingListSerializer):
    book = BookSerializer(read_only=True)
    payments = PaymentBorrowingSerializer(read_only=True, many=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payments",
        )


class BorrowingCreateSerializer(BorrowingSerializer):
    checkout_url = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "book",
            "user",
            "checkout_url",
        )
        read_only_fields = ("borrow_date", "user")

    def get_checkout_url(self, obj):
        response = create_checkout_session(obj)
        return response["url"]

    def validate(self, attrs):
        book = attrs["book"]
        if book.inventory <= 0:
            raise serializers.ValidationError(
                "There are no more books left, try again later"
            )
        book.inventory = book.inventory - 1
        book.save()
        return attrs

    def create(self, validated_data):
        borrowing = super().create(validated_data)
        send_notification(borrowing)
        return borrowing


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


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        ]


class PaymentListSerializer(PaymentSerializer):
    borrowing = BorrowingListSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "borrowing",
            "money_to_pay",
        ]


class PaymentDetailSerializer(PaymentSerializer):
    borrowing = BorrowingListSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        ]


class PaymentSuccessSerializer(PaymentSerializer):
    class Meta:
        model = Payment
        fields = []
