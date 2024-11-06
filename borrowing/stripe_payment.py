import stripe
import os

from borrowing.models import Borrowing, Payment


stripe.api_key = os.environ.get("STRIPE_API_KEY", False)


def create_checkout_session(borrowing: Borrowing) -> stripe.checkout.Session:
    amount_of_days = borrowing.expected_return_date - borrowing.borrow_date
    amount_of_days = amount_of_days.days
    price = borrowing.book.daily_fee * amount_of_days * 100
    stride_price = int(price)

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
        success_url="http://localhost:4242/success",
        cancel_url="http://localhost:4242/cancel",
    )

    data = {
        "status": "Paid",
        "type": "Payment",
        "borrowing": borrowing,
        "session_url": session["url"],
        "session_id": session["id"],
        "money_to_pay": price,
    }

    Payment.objects.create(**data)

    return session
