import boto3
import os
import json

REGION = os.environ.get("REGION")
ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
LAMBDA_BASE_ARN = os.environ.get("LAMBDA_BASE_ARN")

LAMBDA_REDIS_READ_ARN = f"{LAMBDA_BASE_ARN}:retrieve_redis"
LAMBDA_REDIS_WRITE_ARN = f"{LAMBDA_BASE_ARN}:store_redis"

lambda_client = boto3.client(
    "lambda",
    region_name=REGION,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)


def read_from_redis(data={"table": "itemDetails", "key": "all"}):
    payload = json.dumps(data)
    print(payload)

    response = lambda_client.invoke(
        FunctionName=LAMBDA_REDIS_READ_ARN,
        InvocationType="RequestResponse",
        Payload=payload,
    )

    res_payload = json.loads(response["Payload"].read())
    res_body = res_payload["body"]
    if res_body:  # To account for if body = "" and json.loads will stringify it
        res_body = json.loads(res_body)
    return res_body


def write_to_redis(data={"table": "itemDetails", "key": "all"}):
    payload = json.dumps(data)
    print(payload)

    response = lambda_client.invoke(
        FunctionName=LAMBDA_REDIS_WRITE_ARN,
        InvocationType="RequestResponse",
        Payload=payload,
    )

    res_payload = json.loads(response["Payload"].read())
    print(res_payload["statusCode"])

    res_body = res_payload["body"]
    return res_body
