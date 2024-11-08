from rest_framework import generics, status
from rest_framework.response import Response

from borrowing.models import Borrowing, Payment
from borrowing.serializers import (
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
    BorrowingListSerializer,
    BorrowingReturnSerializer,
    BorrowingSerializer,
    PaymentDetailSerializer,
    PaymentListSerializer,
    PaymentSuccessCancelSerializer,
)


class BorrowingListCreateView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingListSerializer

    def get_serializer_class(self):

        if self.request.method == "GET":
            return BorrowingListSerializer

        if self.request.method == "POST":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    def get(self, request, *args, **kwargs):
        """Returns list of all Borrowing instances"""
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Creates an instance of Borrowing model.\n
        Calls send_telegram_notification() method that sends notification
        via telegram bot.\n
        Calls create_checkout_session() to create stripe
        payment session and returns checkout session url.\n
        Decreases a borrowed book inventory by 1 (default quantity)
        """
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class BorrowingRetrieveView(generics.RetrieveUpdateAPIView):
    queryset = Borrowing.objects.select_related(
        "book", "user"
    ).prefetch_related("payments")
    serializer_class = BorrowingDetailSerializer

    def get(self, request, *args, **kwargs):
        """Returns detail info about an instance of Borrowing model"""
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Updates info about an instance of Borrowing model
        (requires all fields to be provided)
        """
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Updates info about an instance of Borrowing model
        (does not require all fields to be provided)
        """
        return super().patch(request, *args, **kwargs)


class BorrowingReturnView(generics.UpdateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingReturnSerializer

    def put(self, request, *args, **kwargs):
        """
        (The same as patch version)\n
        Update actual_return_date to today`s date.\n
        Increases a borrowed book inventory by 1 (default quantity).
        """
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        (The same as put version)\n
        Update actual_return_date to today`s date.\n
        Increases a borrowed book inventory by 1 (default quantity).
        """
        return super().patch(request, *args, **kwargs)


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.select_related(
        "borrowing"
    ).prefetch_related("borrowing__user", "borrowing__book")
    serializer_class = PaymentListSerializer


class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.select_related(
        "borrowing"
    ).prefetch_related("borrowing__user", "borrowing__book")
    serializer_class = PaymentDetailSerializer


class PaymentSuccessView(generics.GenericAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSuccessCancelSerializer

    def patch(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.status = "Paid"
        instance.save()

        return Response(data="Success", status=status.HTTP_200_OK)


class PaymentCancelView(generics.GenericAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSuccessCancelSerializer

    def get(self, request, *args, **kwargs) -> Response:

        data_str = (
            "Payment was canceld. You can try to pay again within 24 hours."
        )

        return Response(
            data=data_str,
            status=status.HTTP_402_PAYMENT_REQUIRED
        )
