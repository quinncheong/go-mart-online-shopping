import boto3
import os

REGION = os.environ.get("REGION")
ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
QUEUE_NAME = os.environ.get("QUEUE_NAME")
DELETE_MESSAGE = True

print(os.environ)

sqs = boto3.resource(
    "sqs",
    region_name=REGION,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)


def send_message_to_queue(message):
    response = queue.send_message(MessageBody=message)
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
