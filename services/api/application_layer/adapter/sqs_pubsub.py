import json
import logging
import boto3

from typing import Optional
from botocore.exceptions import ClientError

logger = logging.getLogger('bhub.' + __name__)


class MessageAnnouncerSQS:

    @classmethod
    def get_queue(cls, name):
        sqs = boto3.resource(service_name='sqs', region_name='us-east-1')

        logger.info(
            'Getting SQS queue',
            extra={
                'props': {
                    'service': 'SQS',
                    'method': 'get_queue',
                    'queue_name': name
                }
            }
        )

        try:

            queue = sqs.get_queue_by_name(QueueName=name)

            logger.info(
                'Got SQS queue successfully',
                extra={
                    'props': {
                        'service': 'SQS',
                        'method': 'get_queue',
                        'queue_name': name,
                        'queue_url': queue.url
                    }
                }
            )

        except ClientError as error:
            logger.exception(
                'Could not get queue',
                extra={
                    'props': {
                        'service': 'SQS',
                        'method': 'get_queue',
                        'queue_name': name
                    }
                }
            )

            raise error
        else:
            return queue

    @classmethod
    def send_message(
            cls,
            name: str,
            message_body: dict,
            message_attributes=None,
            delay_seconds: Optional[int] = None
    ):

        queue = cls.get_queue(name=name)

        if not message_attributes:
            message_attributes = {}

        logger.info(
            'Sending message to SQS queue',
            extra={
                'props': {
                    'service': 'SQS',
                    'method': 'send_message',
                    'message': message_body,
                    'queue_url': queue.url,
                    'delay_seconds': delay_seconds
                }
            }
        )

        try:
            if delay_seconds:
                response = queue.send_message(
                    MessageBody=json.dumps(message_body),
                    MessageAttributes=message_attributes,
                    DelaySeconds=delay_seconds
                )
            else:
                response = queue.send_message(
                    MessageBody=json.dumps(message_body),
                    MessageAttributes=message_attributes
                )

            logger.info(
                'Sent message to SQS queue successfully',
                extra={
                    'props': {
                        'service': 'SQS',
                        'method': 'send_message',
                        'message': message_body,
                        'queue_url': queue.url,
                        'delay_seconds': delay_seconds
                    }
                }
            )

        except ClientError as error:
            logger.exception(
                'Message sent to SQS queue failed',
                extra={
                    'props': {
                        'service': 'SQS',
                        'method': 'send_message',
                        'message': message_body,
                        'queue_url': queue.url,
                        'delay_seconds': delay_seconds
                    }
                }
            )
            raise error
        else:
            return response
