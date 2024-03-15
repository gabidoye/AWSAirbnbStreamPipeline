import json
import boto3
import random
import os
import datetime
import uuid

sqs_client = boto3.client('sqs')
QUEUE_URL = os.getenv('SQS_ARN')   # replace with your SQS Queue URL

def generate_airbnb_booking():
    canadian_cities = [
        "Toronto, Canada",
        "Montreal, Canada",
        "Vancouver, Canada",
        "Calgary, Canada",
        "Edmonton, Canada",
        "Ottawa, Canada",
        "Winnipeg, Canada",
        "Quebec City, Canada",
        "Halifax, Canada",
        "Victoria, Canada",
        "Saskatoon, Canada"
    ]

    start_date = datetime.date(2023, 11, 30)
    end_date = datetime.date(2024, 03, 31)
    booking_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
    duration = datetime.timedelta(days=random.randint(1, 14))

    return {
        "bookingId": str(uuid.uuid4()),
        "userId": f"UserID-{random.randint(1000, 9999)}",
        "propertyId": f"PropertyID-{random.randint(100, 999)}",
        "location": random.choice(canadian_cities),
        "startDate": booking_date.strftime("%Y-%m-%d"),
        "endDate": (booking_date + duration).strftime("%Y-%m-%d"),
        "price": f"{random.randint(50, 500)} USD"
    }

def lambda_handler(event, context):
    i=0
    while(i<200):
        guest_bookings = generate_airbnb_booking()
        print(guest_bookings)
        sqs_client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(guest_bookings)
        )
        i += 1
    
    return {
        'statusCode': 200,
        'body': json.dumps('Guest bookings data published to SQS!')
    }


