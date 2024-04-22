import logging
import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):

    DEBUG = False
    TESTING = False
    DEPLOY_ENV = os.environ.get("DEPLOY_ENV", "Development")
    LOGS_LEVEL = logging.INFO

    LOCALSTACK_URL = os.environ.get("LOCALSTACK_URL", "") or None
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/bhub")
    
    QUEUE_PROCESS_PAYMENTS = os.environ.get("QUEUE_PROCESS_PAYMENTS", "queue-process-payments")


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    LOGS_LEVEL = logging.CRITICAL
    MONGO_URI = "mongodb://server.test.com"


class StagingConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/bhub"
    )


class ProductionConfig(BaseConfig):
    LOGS_LEVEL = int(os.environ.get("LOG_LEVEL",logging.INFO))
