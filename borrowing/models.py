from django.db import models
from django.conf import settings

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} borrows {self.book}"


class Payment(models.Model):

    class StatusChoice(models.TextChoices):
        PENDING = "Pending"
        PAID = "Paid"

    class TypeChoice(models.TextChoices):
        PAYMENT = "Payment"
        FINE = "Fine"

    status = models.CharField(choices=StatusChoice, max_length=7)
    type = models.CharField(choices=TypeChoice, max_length=7)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField(max_length=516)
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.status} {self.type} session"
