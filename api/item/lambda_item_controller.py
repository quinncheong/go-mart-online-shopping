import boto3
import os
import json

session = boto3.Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# Create an instance of the Lambda client
lambda_client = session.client("lambda", region_name="ap-southeast-1")

# Define the name of the Lambda function to be invoked
# retrieve_redis_fn_arn = f"arn:aws:lambda:{region_name}:{account_id}:function:{retrieve_redis_fn_name}"
retrieve_redis_fn_arn = (
    "arn:aws:lambda:ap-southeast-1:377115435266:function:retrieve_redis"
)
# Define the input data to be passed to the Lambda function
input_data = {"id": "73"}

# Invoke the Lambda function and capture the response
response = lambda_client.invoke(
    FunctionName=retrieve_redis_fn_arn,
    InvocationType="RequestResponse",
)

# Extract the response body from the response
response_body = json.loads(response["Payload"].read())

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
        return item_table.scan(Limit=10, ExclusiveStartKey=esk)
    return item_table.scan(Limit=10)


def get_item(item_id=None):
    if not item_id:
        return

    key = {"id": str(item_id)}
    res = item_table.get_item(Key=key)
    print("getItem", res)
    return res if res else None


def get_num_items():
    return connection.describe_table(TableName="item")["Table"]["ItemCount"]


# Process the response body
if response_body["body"] == "[]":
    # Get all items or a specific item based on input data
    if input_data.get("id"):
        data = get_item(input_data["id"])
        data = [data] if data else []
    else:
        data = []
        response = get_all_items()
        while True:
            data += response.get("Items", [])
            if not response.get("LastEvaluatedKey"):
                break
            response = get_all_items(response["LastEvaluatedKey"])

    # Define the name of the Lambda function to store data
    # store_data_fn_arn = f"arn:aws:lambda:{region_name}:{account_id}:function:{store_data_fn_name}"
    store_data_fn_arn = (
        "arn:aws:lambda:ap-southeast-1:377115435266:function:store_redis"
    )

    # Invoke the Lambda function to store the data
    response = lambda_client.invoke(
        FunctionName=store_data_fn_arn,
        InvocationType="RequestResponse",
        Payload=json.dumps(data),
    )

    # Extract the response body from the response
    response_body = json.loads(response["Payload"].read())
print(response_body)
