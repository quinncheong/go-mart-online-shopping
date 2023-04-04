from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import boto3
import json

load_dotenv()

import sns_controller
import stripe_controller
import requests
from invokes import invoke_http

REGION = os.environ.get("REGION")
ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)
CORS(app)


ITEM_URL = os.environ.get("ITEM_URL")
ORDER_URL = os.environ.get("ORDER_URL")
ERROR_URL = os.environ.get("ERROR_URL")

lambda_client = boto3.client(
    "lambda",
    region_name=REGION,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)


@app.route("/")
def hello():
    """
    Health Endpoint
    """
    return "Place-order is OK"


@app.route("/v1/place-order/health")
def health():
    """
    Health Check Endpoint for API Gateway
    """
    return "Place Order connected"


@app.route("/v1/place-order/test/email")
def test_email():
    """
    Test Email to send message
    """
    message = {
        "subject": "Your Order has been placed",
        "emails": [
            "quinncheong.2019.is458.jan2023@gmail.com",
            "alinaatxn@gmail.com",
        ],
        "body": "Your order has been successfully placed!",
    }

    res = sns_controller.send_message_to_sns_topic(message)

    return res if res else "Email not sent"


@app.route("/v1/place-order/test/item")
def test_item():
    """
    Test Email to send message
    """
    print("inside the test request")
    items = requests.get(ITEM_URL + "/v1/item/all").json()
    print(items)
    return items


@app.route("/v1/place-order/test/order")
def test_order():
    """
    Test Email to send message
    """
    print("inside the test order request")
    product_id = requests.get(
        ORDER_URL + "/v1/order/email/" + "test@example.com"
    ).json()
    print(product_id)
    return product_id


@app.route("/v1/place-order/test/sage")
def test_sage():
    """
    Test Email to send message
    """
    print("inside the test sagemake lambda request")

    request_body = json.dumps({"Input": 20})

    # Invoke the Lambda function
    response = lambda_client.invoke(
        FunctionName="ML_Recommendation",
        InvocationType="RequestResponse",
        Payload=request_body,
    )

    # Extract the response body
    res_payload = json.loads(response["Payload"].read())
    print(res_payload)
    return res_payload


@app.route("/v1/place-order", methods=["POST"])
def place_order():
    body = request.get_json()
    print(body)

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
    print("order data:", order_data)

    res = invoke_http(
        ORDER_URL + "/v1/order",
        method="POST",
        json=order_data,
    )

    if res["code"] in range(200, 300):
        message = {
            "subject": "Your Order has been placed",
            "emails": [
                "quinncheong.2019.is458.jan2023@gmail.com",
                "alinaatxn@gmail.com",
            ],
            "body": "Your order has been successfully placed!",
        }

        sns_controller.send_message_to_sns_topic(message)

    # sms_data = json.dumps(data)
    # msg_status = send_sms(sms_data)

    return jsonify(res), res["code"]


@app.route("/v1/place-order/displayItems/<email>")
def displayItems(email: str = None):
    """
    This function returns the item details and also includes if item is recommended
    """

    print(email)
    try:
        items_response = requests.get(ITEM_URL + "/v1/item/all").json()
        items = items_response["Items"]
    except:
        print("No items found")
        return jsonify([]), 200

    if (
        email == "None"
        or email == "null"
        or email == "undefined"
        or email == ""
        or not email
    ):
        return items

    try:
        user_last_purchase_product_id = requests.get(
            ORDER_URL + "/v1/order/email/" + email
        ).json()
        user_last_purchase_product_id = user_last_purchase_product_id["product_id"]
    except:
        print("No previous purchase found")
        return items

    # Get the request body
    request_body = json.dumps({"Input": user_last_purchase_product_id})
    print(request_body)

    # Invoke the Lambda function
    response = lambda_client.invoke(
        FunctionName="ML_Recommendation",
        InvocationType="RequestResponse",
        Payload=request_body,
    )

    # Extract the response body
    res_payload = json.loads(response["Payload"].read())
    print(res_payload)

    if "Output" not in res_payload:
        print("output not found")
        return items

    res_payload = res_payload["Output"]
    for item in items_response["Items"]:
        if int(item["id"]) in res_payload:
            item["Recommendation"] = True
        else:
            item["Recommendation"] = False

    items = items_response["Items"]
    return items


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
