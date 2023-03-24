from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

import sqs_controller
import stripe_controller
from invokes import invoke_http


app = Flask(__name__)
CORS(app)

ORDER_URL = os.environ.get("ORDER_URL")
ERROR_URL = os.environ.get("ERROR_URL")


@app.route("/")
def hello():
    """
    Health Check Endpoint
    """
    return "Place Order connected"


@app.route("/place-order", methods=["POST"])
def place_order():
    body = request.get_json()

    if "order_data" not in body:
        return jsonify("Wrong Order Data"), 404

    if "payment_data" not in body:
        return jsonify("Wrong Payment Data"), 404

    payment_data = body["payment_data"]
    payment_outcome = stripe_controller.make_payment(payment_data)

    if payment_outcome["payment_status"] == "Failed":
        return jsonify("Payment Failed"), 404

    order_data = body["order_data"]
    order_data["payment_id"] = payment_outcome["payment_id"]

    res = invoke_http(
        ORDER_URL + "/order",
        method="POST",
        json=order_data,
    )

    if res["code"] in range(200, 300):
        sqs_controller.send_message_to_queue("Your order has been successful")

    #     message = f"Hi {data['user_name']}, your order was successfully placed!"
    #     data = {"body": message, "to": data["phone_number"]}

    # sms_data = json.dumps(data)
    # msg_status = send_sms(sms_data)

    return jsonify(res), res["code"]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
