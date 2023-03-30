from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import item_controller

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    """
    Health Endpoint
    """
    return "OK"


@app.route("/v1/item/health")
def health():
    """
    Health Check Endpoint for API Gateway
    """
    return "Item connected"


@app.route("/v1/item/all")
def get_items():
    """
    This function gets all items from the database
    """
    return item_controller.get_all_items()


@app.get("/v1/item/<item_id>")
def get_item_by_id(item_id: str = None):
    """
    This function gets a specific item from the database,
    querying by item_id
    """
    return item_controller.get_item(item_id)


@app.route("/v1/item/esk", methods=["POST"])
def query_items_by_esk():
    """
    This function gets items from the database by ExclusiveStartKey (esk).
    esk refers to {"item_name": ""}
    """
    data = request.get_json()

    if "esk" in data:
        esk = data["esk"]
        res = item_controller.get_all_items(esk)
    else:
        res = item_controller.get_all_items()

    return res if res else "No items found/left"


@app.route("/v1/item/get-num-items")
def get_num_items():
    res = item_controller.get_num_items()
    return str(res) if res else "0"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
