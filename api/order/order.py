from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import order_controller
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    """
    Health Check Endpoint
    """
    return "Order connected"


@app.route("/order/all")
def get_all_orders():
    """
    This function gets all orders from the database
    """
    return order_controller.get_all_orders()


@app.route("/order/<order_id>")
def get_order_by_id(order_id: str = None):
    """
    This function gets a specific order from the database,
    querying by order_id
    """
    return order_controller.get_order(order_id)


@app.route("/order", methods=["POST"])
def create_order():
    """
    This function creates a new order in the database
    """
    data = request.get_json(force=True)
    print(data)
    # items_dict = data["items"]

    res = order_controller.add_order(data)
    if res["ResponseMetadata"]["HTTPStatusCode"] in range(200, 300):
        return (
            jsonify(
                {
                    "code": res["ResponseMetadata"]["HTTPStatusCode"],
                    "message": "Order has been added successfully",
                }
            ),
            res["ResponseMetadata"]["HTTPStatusCode"],
        )

    return (
        jsonify(
            {
                "code": res["ResponseMetadata"]["HTTPStatusCode"],
                "message": "Bad request",
            }
        ),
        res["ResponseMetadata"]["HTTPStatusCode"],
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007, debug=True)
