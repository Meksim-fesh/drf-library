from django.urls import path

from borrowing.views import (
    BorrowingListCreateView,
    BorrowingRetrieveView,
    BorrowingReturnView,
    PaymentDetailView,
    PaymentListView,
)

urlpatterns = [
    path(
        "borrowings/",
        BorrowingListCreateView.as_view(),
        name="borrowing-list"
    ),
    path(
        "borrowings/<int:pk>/return/",
        BorrowingReturnView.as_view(),
        name="borrowing-return"
    ),
    path(
        "borrowings/<int:pk>/",
        BorrowingRetrieveView.as_view(),
        name="borrowing-detail"
    ),
    path(
        "payments/",
        PaymentListView.as_view(),
        name="payment-list",
    ),
    path(
        "payments/<int:pk>/",
        PaymentDetailView.as_view(),
        name="payment-detail",
    ),
]

app_name = "borrowing"
