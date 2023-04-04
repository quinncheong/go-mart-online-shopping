import boto3
from boto3.dynamodb.conditions import Key
import os
from datetime import datetime

REGION = os.environ.get("REGION")
ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
TABLE_NAME = "order"


dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

# connection = boto3.client(
#     "dynamodb", REGION, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
# )

order_table = dynamodb.Table(TABLE_NAME)


def get_all_orders(esk={}):
    if esk:
        return order_table.scan(Limit=2, ExclusiveStartKey=esk)
    return order_table.scan(Limit=2)


def get_order(order_id=None):
    if not order_id:
        return

    key = {"id": int(order_id)}
    res = order_table.get_item(Key=key)
    if res and "Item" in res:
        return res["Item"]
    return None


def get_productID(email):
    res = order_table.scan(
        FilterExpression="email = :email",
        ExpressionAttributeValues={":email": email},
        ProjectionExpression="id, product_ids",
    )
    sorted_items = sorted(res["Items"], key=lambda x: x["id"], reverse=True)

    if len(sorted_items) > 0:
        x = sorted_items[0]["product_ids"][0]
        value = list(x.keys())[0]
        return {"product_id": value}

    return None


def add_order(order):
    date = datetime.now().strftime("%b %d, %Y %H:%M:%S")

    # order_id = datetime.now().strftime("%s")
    response = order_table.scan(Select="COUNT")
    order_id = response["Count"] + 1

    to_insert = {"id": order_id, "product_ids": order["product_ids"]}
    if "email" in order:
        to_insert["email"] = order["email"]

    print(to_insert)

    order_table.put_item(Item=to_insert)
    res = order_table.query(KeyConditionExpression=Key("id").eq(order_id))

    # with order_table.batch_writer() as batch:
    #     for item_name, item_quantity in items_dict.items():
    #         batch.put_item(
    #             Item={
    #                 "order_id": order_id,
    #                 "user_email": email,
    #                 "order_date": str(date),
    #                 "item_name": item_name,
    #                 "item_quantity": item_quantity,
    #             }
    #         )
    # res = order_table.query(KeyConditionExpression=Key("id").eq(order_id))
    return res


# def get_num_items():
#     return connection.describe_table(TableName=TABLE_NAME)["Table"]["ItemCount"]
