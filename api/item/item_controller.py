import boto3
import os

import lambda_controller

REGION = os.environ.get("REGION")
ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

connection = boto3.client(
    "dynamodb", REGION, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
)

item_table = dynamodb.Table("itemDetails")


def get_all_items():
    redis_payload = {"table": "itemDetails", "key": "all"}
    redis_data = lambda_controller.read_from_redis(redis_payload)
    if redis_data:
        print("redis:", redis_data)
        return redis_data

    print("Cache Miss")

    table_data = item_table.scan(Limit=2)
    if table_data and "Items" in table_data:
        redis_payload["data"] = table_data
        write_result = lambda_controller.write_to_redis(redis_payload)
        print("Write Result is: ", write_result)

    return table_data


def get_item(item_id=None):
    if not item_id:
        return

    redis_payload = {"table": "itemDetails", "key": item_id}
    redis_data = lambda_controller.read_from_redis(redis_payload)
    if redis_data:
        print(redis_data)
        return redis_data

    print("Cache Miss")

    key = {"id": str(item_id)}
    table_data = item_table.get_item(Key=key)

    if table_data and "Item" in table_data:
        redis_payload["data"] = table_data["Item"]
        write_result = lambda_controller.write_to_redis(redis_payload)
        print("Write Result is: ", write_result)

    return table_data
