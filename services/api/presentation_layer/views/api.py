import logging
from flask import Blueprint, request
from flask_restx import Api, Resource
from json import loads

from api.presentation_layer.views.mapping import PaymentCreateMapping
from api.application_layer.use_cases.payment import PaymentUseCase
from api.presentation_layer.views.schemas import create_payment_model

logger = logging.getLogger("bhub." + __name__)

VERSION = "1.0"
DOC = "API Bhub Index"

bp_index = Blueprint("index", __name__, url_prefix="/")

api = Api(
    bp_index,
    version=VERSION,
    title="API Bhub Index",
    description=DOC,
    doc=False,
)

ns = api.namespace("", description="API Bhub Index")
api.models[create_payment_model.name] = create_payment_model

@ns.route("/", "/health", doc=False)
class Index(Resource):
    def get(self):
        return dict(service="API Bhub HealthCheck", version=VERSION)
    
@ns.route("/payment")
class Create(Resource):
    @ns.expect(create_payment_model, validate=True)
    @ns.response(200, 'OK')
    @ns.response(400, 'Request failed')
    def post(self):

        payload = loads(request.data)
        mapping = PaymentCreateMapping(payload=payload)
        
        try:
            payment = PaymentUseCase.create_payment(data=mapping)
            
            return {"message": f"Payment {payment.id} created successfully"}, 201
        except Exception as e:

            logger.exception(
                "Failed to create Client",
                extra={
                    "props": {
                        "request": "/clients/",
                        "method": "POST",
                        "type": mapping.type,
                        "value": mapping.value,
                        "cliente_uuid": mapping.client_uuid,
                        "callback_url": mapping.callback_url,
                        "error_message": str(e),
                    }
                },
            )
            return {'message': 'Error on create payment'}, 500 
    