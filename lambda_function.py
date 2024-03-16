import boto3
import os
import json
import pandas as pd
from datetime import datetime

def filter_records(message_body):
    """
    Filters booking records based on the duration of the stay.
    
    Args:
        message_body (dict): A dictionary containing the details of a booking.
    
    Returns:
        pandas.DataFrame: A DataFrame containing the booking details if the booking duration is more than 1 day; otherwise, an empty DataFrame.
    """
    # Normalize the message body into a pandas DataFrame for easy manipulation
    message_df = pd.json_normalize(message_body)
    
    # Convert start and end dates to pandas datetime objects
    start_date = pd.to_datetime(message_df['startDate'])
    end_date = pd.to_datetime(message_df['endDate'])
    
    # Calculate the duration of the booking in days
    duration = (end_date - start_date).dt.days
    
    # Print and return the appropriate DataFrame based on the booking duration
    if duration.iloc[0] > 1:
        print("Processing booking with duration more than 1 day: ", message_body)
        return message_df
    else:
        print("Skipping booking with duration of 1 day or less.")
        return pd.DataFrame()

def lambda_handler(event, context):
    """
    AWS Lambda function handler to process messages from an SQS queue,
    filter them based on booking duration, and store the filtered records in an S3 bucket.
    
    Args:
        event: The event dict that triggers the lambda function.
        context: The context in which the lambda function is called.
    
    Returns:
        dict: A dictionary with the status code and a message indicating the outcome of the operation.
    """
    print("Starting SQS Batch Process")
    
    # Retrieve the SQS queue URL and the target S3 bucket name from environment variables
    queue_url = os.getenv('SQS_URL')
    target_bucket_name = os.getenv('target_bucket_name')

    # Initialize AWS SQS and S3 clients
    sqs = boto3.client('sqs')
    s3_client = boto3.client('s3')

    # Receive messages from the SQS queue with long polling
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,  # Adjust this value based on your use case
        WaitTimeSeconds=5       # Long polling for 5 seconds
    )

    messages = response.get('Messages', [])
    print("Total messages received in the batch: ", len(messages))

    # List to accumulate DataFrame objects for each message that passes the filter
    filtered_records_list = []

    for message in messages:
        message_body = json.loads(message['Body'])
        print("Received message: ", message_body)

        # Filter the records based on the booking duration
        filtered_df = filter_records(message_body)

        # If the DataFrame is not empty, add it to the list
        if not filtered_df.empty:
            filtered_records_list.append(filtered_df)

        # Delete the processed message from the queue
        receipt_handle = message['ReceiptHandle']
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

    # If there are any filtered records, concatenate them into a single DataFrame
    if filtered_records_list:
        filtered_records = pd.concat(filtered_records_list, ignore_index=True)
        # Convert the DataFrame to JSON bytes
        filtered_json = filtered_records.to_json(orient='records', date_format='iso')
        filtered_json_bytes = filtered_json.encode('utf-8')

        # Create a file name with the current date and upload the JSON to S3
        current_date = datetime.now().strftime("%Y-%m-%d")
        target_file_key = f'filtered_records_{current_date}.json'
        s3_client.put_object(Bucket=target_bucket_name, Key=target_file_key, Body=filtered_json_bytes)
        print(f"Filtered records written to {target_bucket_name}/{target_file_key}")

    print("Ending SQS Batch Process")
    
    return {
        'statusCode': 200,
        'body': f'{len(messages)} messages processed. Filtered records stored in S3.'
    }
