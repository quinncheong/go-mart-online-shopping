from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import item_controller

load_dotenv("./.env")

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    """
    Health Check Endpoint
    """
    return "Item connected"


@app.route("/item/all")
def get_items():
    """
    This function gets all items from the database
    """
    return item_controller.get_all_items()


@app.get("/item/<item_id>")
def get_item_by_id(item_id: str = None):
    """
    This function a specific item from the database,
    querying by item_id
    """
    return item_controller.get_item(item_id)


@app.route("/get-all-items", methods=["POST"])
def get_all_items():
    data = request.get_json()

    # esk refers to {"item_name": ""}
    if "esk" in data:
        esk = data["esk"]
        print("hello")
        print(esk)
        res = item_controller.get_all_items(esk)["Items"]
    else:
        res = item_controller.get_all_items()["Items"]

    return res if res else "No items found/left"


@app.route("/get-item", methods=["POST"])
def get_item():
    data = request.get_json()
    key = data["key"]
    res = item_controller.get_item(key)
    return res if res else "No items found/left"


@app.route("/get-num-items", methods=["GET"])
def get_num_items():
    res = item_controller.get_num_items()
    return str(res) if res else "0"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
