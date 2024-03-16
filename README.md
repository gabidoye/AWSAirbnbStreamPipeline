# AirBnB Stream Data Ingestion Pipeline
## Objective
This project aims to construct a simulated data pipeline leveraging AWS services to handle Airbnb booking data. It showcases the capabilities for real-time data ingestion, processing, filtering, and storage in a cloud environment, offering a practical example of managing and analyzing booking information dynamically.

## Overview
The pipeline integrates various AWS services, including AWS Lambda, Amazon SQS, Amazon S3, AWS CodeBuild, and Amazon EventBridge, to create a robust and scalable data processing workflow. By simulating the flow of Airbnb booking data through this pipeline, we demonstrate how to efficiently process, filter, and store data in real-time, ensuring only relevant records are persisted for analysis.

## Prerequisites
To deploy and test this pipeline, you'll need:

An active AWS Account.
A basic understanding of AWS services such as Lambda, SQS, S3, CodeBuild, and EventBridge.
Familiarity with the AWS CLI or Management Console.
Knowledge of Python programming, particularly for writing Lambda functions.
Architecture
This project is structured into several key components, each fulfilling a specific role in the data processing workflow:

### Part 1: SQS Queue Setup with DLQ
AirbnbBookingQueue: An SQS Standard Queue to receive incoming mock Airbnb booking data.
AirbnbBookingDLQ: A Dead Letter Queue configured to capture messages from AirbnbBookingQueue after 3 unsuccessful delivery attempts, ensuring no data is lost unintentionally.

### Part 2: Producer Lambda Function
ProduceAirbnbBookingData: A Lambda function responsible for generating and publishing mock Airbnb booking data to the AirbnbBookingQueue.

### Part 3: EventBridge Integration
An EventBridge rule to consume messages from AirbnbBookingQueue and filter out messages based on specific criteria, such as booking duration exceeding one day.

### Part 4: Consumer Lambda Function
ProcessFilteredBookings: A Lambda function triggered by the EventBridge rule to process and store filtered booking records in an S3 bucket named airbnb-booking-records.

### Part 5: CI/CD with AWS CodeBuild
Setup a CodeBuild project linked to your GitHub repository to automate the deployment of updates to your Lambda functions, ensuring a smooth development workflow.


## Getting Started
Setup Instructions
SQS and DLQ Configuration: Follow the AWS documentation to create your SQS queues and configure the DLQ settings.

Lambda Functions: Deploy the Producer and Consumer Lambda functions using the provided Python scripts. Ensure the correct IAM roles and permissions are assigned for accessing SQS and S3.

EventBridge Rule: Create an EventBridge rule targeting the AirbnbBookingQueue with the specified filtering logic for booking duration.

S3 Bucket Preparation: Create an S3 bucket named airbnb-booking-records to store the processed booking data.

CodeBuild Project: Configure your AWS CodeBuild project to connect to your GitHub repository and set up the build specifications as outlined.

## Deployment
Refer to the buildspec.yml for the detailed build and deployment process. Make sure to adjust the environment variables and IAM permissions according to your AWS setup.

## Contribution
Contributions are welcome! If you have suggestions for improving this pipeline or have found a bug, please open an issue or submit a pull request.

