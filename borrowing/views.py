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

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class BorrowingRetrieveView(generics.RetrieveUpdateAPIView):
    queryset = Borrowing.objects.select_related(
        "book", "user"
    ).prefetch_related("payments")
    serializer_class = BorrowingDetailSerializer


class BorrowingReturnView(generics.UpdateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingReturnSerializer


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer


class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
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
