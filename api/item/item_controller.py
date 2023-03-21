import boto3
import os

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


def get_all_items(esk={}):
    if esk:
        return item_table.scan(Limit=2, ExclusiveStartKey=esk)
    return item_table.scan(Limit=2)


def get_item(item_id=None):
    if not item_id:
        return

    key = {"id": str(item_id)}
    res = item_table.get_item(Key=key)
    return res["Item"] if res else None


def get_num_items():
    return connection.describe_table(TableName="item")["Table"]["ItemCount"]
