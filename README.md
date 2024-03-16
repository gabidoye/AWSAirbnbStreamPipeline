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
This project is structured into several key components, each fulfilling a specific role in the data processing workflow.

## Architecture Overview:
The AirBnB Stream Data Ingestion system is designed to automate the process of ingesting, processing, and storing Airbnb booking data. It employs a sequence of AWS services that work together to handle data flow, transformation, and storage.

<img width="562" alt="image" src="https://github.com/gabidoye/AWSAirbnbStreamPipeline/assets/86935340/bff6ff57-72c2-460a-b695-bf903bf29a15">


## Process Flow:
#### Producer Lambda Function:

This is the starting point of the pipeline, where the Producer Lambda function generates or receives Airbnb booking data.
The generated data is then sent to an Amazon SQS queue for temporary storage and queuing. This allows for decoupling of data production and consumption, providing a buffer that handles incoming data at scale.

#### Amazon SQS (Simple Queue Service) with DLQ:

The SQS service acts as a message queuing system that temporarily stores the booking data pushed by the Producer.
It ensures that the messages are securely held until they can be processed, handling any fluctuations in load and preventing data loss.A Dead Letter Queue configured to capture messages from AirbnbBookingQueue after 3 unsuccessful delivery attempts, ensuring no data is lost unintentionally.

#### Amazon EventBridge:

EventBridge provides event-driven processing capabilities.
It receives messages from the SQS queue and applies any defined rules to filter and transform the data. For instance, it may filter messages based on booking duration as specified in the system requirements.

#### Consumer Lambda Function:

Triggered by EventBridge, the Consumer Lambda function processes the filtered booking messages.
It performs the final transformation and business logic on the data before it is ready to be stored.

#### Amazon S3 (Simple Storage Service):

The processed booking records are stored in Amazon S3, a highly available and durable object storage service.
The Consumer Lambda function writes the records into an S3 bucket, ensuring that the processed data is securely saved and can be accessed or analyzed later.

#### AWS CodeBuild: 
CodeBuild to automate the build and deployment (CI-CD) process for the Lambda functions based on changes in source repository. Refer to the buildspec.yml for the detailed build and deployment process. Make sure to adjust the environment variables and IAM permissions according to your AWS setup.

## Execution Steps:
Step 1: The Producer Lambda function is invoked, which generates or collects Airbnb booking data.
Step 2: The booking data is sent to an Amazon SQS queue where it is queued for processing.
Step 3: Amazon EventBridge polls the SQS queue and receives the messages, applying any filters or transformations as needed.
Step 4: The Consumer Lambda function is triggered by EventBridge with the filtered data.
Step 5: The Consumer processes the data and writes the final output to an Amazon S3 bucket where the data is stored for long-term retention and analysis.
This architecture provides a robust and scalable solution for handling data workflows, leveraging AWS services for each step in the pipeline to ensure a smooth and efficient data processing lifecycle.



## Contribution
Contributions are welcome! If you have suggestions for improving this pipeline or have found a bug, please open an issue or submit a pull request.

