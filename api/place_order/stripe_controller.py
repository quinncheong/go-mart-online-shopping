import os
import logging
from invokes import invoke_http


log = logging.getLogger("stripe_controller.sub")

PAYMENT_URL = os.environ.get("PAYMENT_URL") or "http://localhost:5006"


def make_payment(data):
    payment_intent = invoke_http(
        PAYMENT_URL + "/v1/stripe-wrapper/pay", method="POST", json=data
    )
    print(payment_intent)

    payment_outcome = {"payment_id": "", "payment_status": ""}

    if "success" in payment_intent:
        payment_outcome["payment_id"] = payment_intent["payment_id"]
        payment_outcome["payment_status"] = "Paid"
    else:
        payment_outcome["payment_status"] = "Failed"

    return payment_outcome
