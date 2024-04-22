import boto3
import os

sqs_client = boto3.client(
    'sqs',
    aws_access_key_id='ACCESS_KEY',
    aws_secret_access_key='SECRET_ACCESS_KEY',
)