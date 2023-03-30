#! /usr/bin/env python3.6
"""
Python 3.6 or newer required.
"""
from flask_cors import CORS
from flask import Flask, render_template, jsonify, request
import json
import stripe
import os

from dotenv import load_dotenv

load_dotenv()

# This is your test secret API key.
stripe.api_key = os.environ.get("STRIPE_API_KEY")


app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    """
    Health Endpoint
    """
    return "OK"


@app.route("/v1/stripe-wrapper/health")
def health():
    """
    Health Endpoint for API Gateway
    """
    return "Stripe Wrapper Connected"


# AJAX endpoint when `/pay` is called from client
@app.route("/v1/stripe-wrapper/pay", methods=["POST"])
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
            )
        elif "payment_intent_id" in data:
            intent = stripe.PaymentIntent.confirm(data["payment_intent_id"])
    except stripe.error.CardError as e:
        # Display error on client
        app.logger.info(intent)
        return json.dumps({"error": e.user_message}), 200

    print(intent)

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
