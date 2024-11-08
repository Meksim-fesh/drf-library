import os
import json
import requests

from borrowing.models import Borrowing


TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", False)
USER_TO_SEND_NOTIFICATION_ID = os.environ.get("TELEGRAM_USER_ID", False)
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
}


def send_telegram_notification(borrowing: Borrowing) -> requests.Response:
    if not (TELEGRAM_TOKEN and USER_TO_SEND_NOTIFICATION_ID):
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": USER_TO_SEND_NOTIFICATION_ID,
        "text": (
            f"Borrowing with id {borrowing.id} created:\n"
            f"Borrow date: {borrowing.borrow_date}\n"
            f"Expected return date: {borrowing.expected_return_date}\n"
            f"Book: {borrowing.book}\n"
            f"User: {borrowing.user}"
        ),
    }
    pyaload_json = json.dumps(payload)

    response = requests.request(
        "POST", url, headers=DEFAULT_HEADERS, data=pyaload_json
    )

    return response
