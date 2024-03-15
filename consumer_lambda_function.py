import boto3
import os

def lambda_handler(event, context):
    print("Starting SQS Batch Process")
    # Specify your SQS queue URL
    queue_url = os.getenv ('SQS_URL')

    # Create SQS client
    sqs = boto3.client('sqs')

    # Receive messages from the SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,  # Adjust based on your preference
        WaitTimeSeconds=30      # Use long polling
    )

    messages = response.get('Messages', [])
    print("Total messages received in the batch : ",len(messages))
    for message in messages:
        # Process message
        print("Processing message: ", message['Body'])

        # Delete message from the queue
        receipt_handle = message['ReceiptHandle']
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print("Message deleted from the queue")
        
    print("Ending SQS Batch Process")

    return {
        'statusCode': 200,
        'body': f'{len(messages)} messages processed and deleted successfully'
    }