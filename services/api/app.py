import logging
import os
import sys

import click
import flask_pymongo
import json_logging
from flask import Flask
from flask_cors import CORS

ENV = os.environ.get("DEPLOY_ENV", "Development")
mongo_client = flask_pymongo.PyMongo()

def create_app(env: str = ENV) -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(f"api.config.{env}Config")

    __register_blueprints_and_error_handling(app)
    __configure_logger(app)
    __configure_lendico_services(app)

    if app.testing:
        from mongomock import MongoClient

        mongo_client.cx = MongoClient()
        mongo_client.db = mongo_client.cx["BHUB"]

    mongo_client.init_app(app)

    return app


def __register_blueprints_and_error_handling(app: Flask):
    from api.presentation_layer.views.api import bp_index
    
    app.register_blueprint(bp_index)


def __configure_logger(app: Flask):
    if not json_logging.ENABLE_JSON_LOGGING:
        json_logging.init_flask(enable_json=True)
        json_logging.init_request_instrument(app)

    logger = logging.getLogger("api-bhub")
    logger.setLevel(app.config["LOGS_LEVEL"])
    logger.addHandler(logging.StreamHandler(sys.stdout))


def __configure_lendico_services(app: Flask):
    pass
