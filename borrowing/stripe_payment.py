import stripe
import os

from rest_framework.reverse import reverse

from borrowing.models import Borrowing, Payment
from library_system.settings import BASE_URL


stripe.api_key = os.environ.get("STRIPE_API_KEY", False)


def create_checkout_session(borrowing: Borrowing) -> stripe.checkout.Session:
    amount_of_days = borrowing.expected_return_date - borrowing.borrow_date
    amount_of_days = amount_of_days.days
    price = borrowing.book.daily_fee * amount_of_days
    stride_price = int(price * 100)

    data = {
        "status": "Pending",
        "type": "Payment",
        "borrowing": borrowing,
        "money_to_pay": price,
    }
    payment = Payment.objects.create(**data)

    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": borrowing.book
                    },
                    "unit_amount": stride_price,
                },
                "quantity": 1
            }
        ],
        mode="payment",
        success_url=(
            f"{BASE_URL}"
            f"{reverse("borrowing:payment-success", args=[payment.id])}"
        ),
        cancel_url="http://localhost:4242/cancel",
    )

    payment.session_url = session.url
    payment.session_id = session.id
    payment.save()

    return session
