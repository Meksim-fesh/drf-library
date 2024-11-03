from django.urls import path

from borrowing.views import (
    BorrowingListCreateView,
    BorrowingRetrieveView,
    BorrowingReturnView,
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
]

app_name = "borrowing"
