from django.urls import path

from borrowing.views import (
    BorrowingListCreateView,
    BorrowingRetrieveView,
    BorrowingReturnView,
    PaymentCancelView,
    PaymentDetailView,
    PaymentListView,
    PaymentSuccessView,
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
    path(
        "payments/<int:pk>/success/",
        PaymentSuccessView.as_view(),
        name="payment-success",
    ),
    path(
        "payments/<int:pk>/cancel/",
        PaymentCancelView.as_view(),
        name="payment-cancel",
    ),
]

app_name = "borrowing"
