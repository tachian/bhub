import json
import os
import boto3
import pytest

from unittest import mock
from botocore.exceptions import ClientError
from moto import mock_aws

from api.application_layer.adapter.sqs_pubsub import MessageAnnouncerSQS
from api.tests.fixtures.payloads import REQUEST_PAYMENT_PROCESS

QUEUE_NAME = 'queue-process-payments'


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture(scope="function")
def aws(aws_credentials):
    with mock_aws():
        yield boto3.client("s3", region_name="us-east-1")


def _setup_sqs_queue(queue_name):
    sqs = boto3.resource('sqs')
    queue = sqs.create_queue(QueueName=queue_name)
    return queue


def test_get_queue_name(aws, app):
    queue_setup = _setup_sqs_queue(QUEUE_NAME)
    queue = MessageAnnouncerSQS.get_queue(name=QUEUE_NAME)

    assert queue == queue_setup


def test_get_queue_name_exceptions(aws, app):
    _setup_sqs_queue(QUEUE_NAME)

    with pytest.raises(ClientError) as e:
        MessageAnnouncerSQS.get_queue(name='not-exists')

    error = e.value
    assert error.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue'


@mock.patch.object(MessageAnnouncerSQS, 'get_queue')
def test_send_message_sqs_queue(
        get_queue_mock,
        aws
):
    queue = _setup_sqs_queue(QUEUE_NAME)

    get_queue_mock.return_value = queue

    MessageAnnouncerSQS.send_message(
        name=QUEUE_NAME,
        message_body=REQUEST_PAYMENT_PROCESS
    )

    messages = queue.receive_messages(
        MessageAttributeNames=['All'],
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )

    assert messages[0].body == json.dumps(REQUEST_PAYMENT_PROCESS)


@mock.patch.object(MessageAnnouncerSQS, 'get_queue')
def test_send_message_sqs_queue_with_delay_seconds(
        get_queue_mock,
        aws
):
    queue = _setup_sqs_queue(QUEUE_NAME)

    get_queue_mock.return_value = queue

    MessageAnnouncerSQS.send_message(
        name=QUEUE_NAME,
        message_body=REQUEST_PAYMENT_PROCESS,
        delay_seconds=1
    )

    messages = queue.receive_messages(
        MessageAttributeNames=['All'],
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )

    assert messages[0].body == json.dumps(REQUEST_PAYMENT_PROCESS)


@mock.patch.object(MessageAnnouncerSQS, 'get_queue')
def test_send_message_sqs_queue_exceptions(
        get_queue_mock,
        aws
):
    queue = _setup_sqs_queue(QUEUE_NAME)

    get_queue_mock.return_value = queue

    with pytest.raises(ClientError) as e:
        MessageAnnouncerSQS.send_message(
            name=QUEUE_NAME,
            message_body=REQUEST_PAYMENT_PROCESS,
            message_attributes={
                'öther_encodings': {'DataType': 'String', 'StringValue': 'str'},
            },
        )

    error = e.value
    assert error.response['Error']['Code'] == 'MessageAttributesInvalid'
