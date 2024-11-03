from rest_framework import generics

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
    BorrowingListSerializer,
    BorrowingReturnSerializer,
    BorrowingSerializer,
)


class BorrowingListCreateView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
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
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer


class BorrowingReturnView(generics.UpdateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingReturnSerializer
