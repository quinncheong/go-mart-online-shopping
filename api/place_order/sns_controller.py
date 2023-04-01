import boto3
import os
import json

REGION = os.environ.get("REGION")
ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")
DELETE_MESSAGE = True

# Create me a SNS client to publish messages to SNS topic
sns = boto3.client(
    "sns",
    region_name=REGION,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)


def send_message_to_sns_topic(message: dict):
    json_message = json.dumps(message)

    # Publish a message to the topic
    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=json_message,
        Subject="New Order",
    )

    print(response)
    return response


# # Receive messages from the queue
# response = sqs.receive_message(
#     QueueUrl=queue_url,
#     AttributeNames=[
#         'SentTimestamp'
#     ],
#     MaxNumberOfMessages=1,
#     MessageAttributeNames=[
#         'All'
#     ],
#     VisibilityTimeout=0,
#     WaitTimeSeconds=0
# )

# # Print out the messages
# if 'Messages' in response:
#     message = response['Messages'][0]
#     print(message['Body'])

# Sample Message Schema
x = {
    "messageId": "ad91d2c0-52a7-41b9-a7c6-eed3d3497d92",
    "receiptHandle": "",
    "body": '{\n  "Type" : "Notification",\n  "MessageId" : "0307bc0b-c7d5-524e-b462-e0a9cdf7bd18",\n  "TopicArn" : "arn:aws:sns:ap-southeast-1:377115435266:TransactionsTopic",\n  "Subject" : "New Order",\n  "Message" : "Your order has been successful",\n  "Timestamp" : "2023-04-01T10:30:58.691Z",\n  "SignatureVersion" : "1",\n  "Signature" : "W4xeurbQtKd0y8u2peX5LJ1LiDLZuQgDdlPJi77gUMEVgE2FPjRGbBi5wxd5GweaaqdWIutqJ/707jDqTTwgzZYW14S2lKKvOYBp1hZpS2OooFHzgK3VZ4O6OYT+kwCUbXhd4rs+LVUzdgpGvHjQPftPz8zlC0wkMy2Vlj4ASPGTMHdB2/K/fM7CsFRHF0Savrymbcw8oCpWOqF3Zp2CeaJ8WHux6/aYGOwiwvsLhlAsFvgVPRQ2qn3XGBV/IbfNs3p0hHlztUgNfGax2ASe/5WbigwKO1i8OKAa/BwiEShLx0jAriTDlg9nyhTQ9cZAJZC65UgQZJ2Lky2NHKY2qg==",\n  "SigningCertURL" : "https://sns.ap-southeast-1.amazonaws.com/SimpleNotificationService-56e67fcb41f6fec09b0196692625d385.pem",\n  "UnsubscribeURL" : "https://sns.ap-southeast-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:ap-southeast-1:377115435266:TransactionsTopic:bd605656-2d44-4e18-8f63-0c41baf05df9"\n}',
    "attributes": {
        "ApproximateReceiveCount": "45",
        "SentTimestamp": "1680345058723",
        "SenderId": "AIDAJDKHOOGYTFNBBCJTW",
        "ApproximateFirstReceiveTimestamp": "1680345058723",
    },
    "messageAttributes": {},
    "md5OfBody": "2310c83b7927339cdc120dfe986a22f7",
    "eventSource": "aws:sqs",
    "eventSourceARN": "arn:aws:sqs:ap-southeast-1:377115435266:TransactionsQueue",
    "awsRegion": "ap-southeast-1",
}
