import boto3
import os
import json
import pandas as pd
from datetime import datetime


def filter_records(message_body):
    """
    Filters records based on booking duration greater than 1 day.

    :param message_body: The body of the message containing booking details.
    :return: A DataFrame with filtered records or an empty DataFrame.
    """
    # Convert the message into a DataFrame
    message_df = pd.json_normalize(message_body)
    # Convert dates to datetime and calculate duration
    message_df['startDate'] = pd.to_datetime(message_df['startDate'])
    message_df['endDate'] = pd.to_datetime(message_df['endDate'])
    message_df['duration'] = (message_df['endDate'] - message_df['startDate']).dt.days
    
    # Filter and return records with duration > 1 day
    return message_df[message_df['duration'] > 1]





def lambda_handler(event, context):
    print("Starting SQS Batch Process")
    # Specify your SQS queue URL
    queue_url = os.getenv ('SQS_URL')

    # Create SQS client
    sqs = boto3.client('sqs')

    # Create S3 client
    s3_client = boto3.client('s3')
    target_bucket_name = os.getenv ('target_bucket_name')

    # Receive messages from the SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,  # Adjust based on your preference
        WaitTimeSeconds=5      # Use long polling
    )

    messages = response.get('Messages', [])
    print("Total messages received in the batch : ",len(messages))

    # Initialize an empty DataFrame for storing filtered records
    filtered_records = pd.DataFrame()

    for message in messages:
        # Process message
        message_body = json.loads(message['Body'])
        print("Received message: ", message_body)

        # Apply filter function
        filtered_df = filter_records(message_body)

        # Append filtered records to the aggregated DataFrame
        filtered_records = filtered_records.append(filtered_df, ignore_index=True)

        # Delete message from the queue
        receipt_handle = message['ReceiptHandle']
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

    # Check if there are any filtered records to write to S3
    if not filtered_records.empty:
        # Convert to JSON bytes
        filtered_json = filtered_records.to_json(orient='records', date_format='iso')
        filtered_json_bytes = filtered_json.encode('utf-8')

        # Define a target file key for the S3 object
        target_file_key = 'filtered_records.json'

        # Write to S3
        s3_client.put_object(Bucket=target_bucket_name, Key=target_file_key, Body=filtered_json_bytes)
        print(f"Filtered records written to {target_bucket_name}/{target_file_key}")

    print("Ending SQS Batch Process")
    return {
        'statusCode': 200,
        'body': f'{len(messages)} messages processed. Filtered records stored in S3.'
    }