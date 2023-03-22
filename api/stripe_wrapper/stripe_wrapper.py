#! /usr/bin/env python3.6
"""
Python 3.6 or newer required.
"""
from flask_cors import CORS
from flask import Flask, render_template, jsonify, request
import json
import stripe

# This is your test secret API key.
stripe.api_key = "sk_test_51KegmTDlqIwRfGLSQlbxGkVbDTOlUTPyXZd6vFmOFGtlctJbEW1nw6FZIosaUu8jTyvSCRCrgrdha4fuVNX4E8ta00aua1NuKC"


app = Flask(__name__)
CORS(app)


# AJAX endpoint when `/pay` is called from client
@app.route("/pay", methods=["POST"])
def pay():
    data = request.get_json()
    intent = None

    try:
        if "payment_method_id" in data:
            # Create the PaymentIntent
            intent = stripe.PaymentIntent.create(
                payment_method=data["payment_method_id"],
                amount=data["amount"],
                currency="sgd",
                confirmation_method="manual",
                confirm=True,
                description=data["order_id"],
            )
        elif "payment_intent_id" in data:
            intent = stripe.PaymentIntent.confirm(data["payment_intent_id"])
    except stripe.error.CardError as e:
        # Display error on client
        app.logger.info(intent)
        return json.dumps({"error": e.user_message}), 200

    return generate_response(intent)


def generate_response(intent):
    # Note that if your API version is before 2019-02-11, 'requires_action'
    # appears as 'requires_source_action'.
    if (
        intent.status == "requires_action"
        and intent.next_action.type == "use_stripe_sdk"
    ):
        # Tell the client to handle the action
        return (
            json.dumps(
                {
                    "requires_action": True,
                    "payment_intent_client_secret": intent.client_secret,
                }
            ),
            200,
        )
    elif intent.status == "succeeded":
        # The payment didn’t need any additional actions and completed!
        # Handle post-payment fulfillment
        app.logger.info(intent)
        return (
            json.dumps(
                {
                    "success": True,
                    "order_id": intent["description"],
                    "payment_id": intent["charges"]["data"][0]["id"],
                }
            ),
            200,
        )
    else:
        # Invalid status from stripe
        app.logger.info(intent)
        return json.dumps({"error": 500, "data": intent}), 500


# @app.route("/refund", methods=['POST'])
# def create_refund():
#     data = request.get_json()
#     payment_id = data['payment_id']
#     try:
#         refund = stripe.Refund.create(
#             # charge='ch_3Kf5qWDlqIwRfGLS0H5iCByJ',
#             charge=payment_id,
#         )
#         return jsonify({
#             'status': refund['status'],
#         })
#     except Exception as e:
#         return jsonify(error=str(e)), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
