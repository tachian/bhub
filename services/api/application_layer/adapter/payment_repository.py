import logging
import pymongo
from uuid import UUID

from api.app import mongo_client
from api.domain_layer.models.payment import PaymentTypeEnum, Payment

logger = logging.getLogger("bhub." + __name__)

class PaymentsRepository:
    
    @classmethod
    def persist_payment(cls, payment: Payment):
        
        logger.info(
            "Persisting payment",
            extra={
                "props": {
                    "method": "persist_payment",
                    "type": str(payment.type),
                    "value": payment.value,
                    "client_uuid": payment.client_uuid,
                    "callback_url": payment.callback_url
                }
            }
        )

        try:
            data = {
                "type": payment.type,
                "value": payment.value,
                "client_uuid": payment.client_uuid,
                "callback_url": payment.callback_url
            }

            result = mongo_client.db.Payments.insert_one(
                {k: v for k, v in data.items() if v is not None}
            )

            logger.info(
                "Payment created",
                extra={
                    "props": {
                        "method": "persist_payment",
                        "id": str(result.inserted_id),
                        "type": str(payment.type),
                        "value": payment.value,
                        "client_uuid": payment.client_uuid,
                        "callback_url": payment.callback_url
                    }
                }
            )
            
            return str(result.inserted_id)

        except Exception as e:
            logger.exception(
                "Error persisting payment",
                extra={
                    "props": {
                        "service": "PaymentsRepository",
                        "method": "persist_payment",
                        "type": str(payment.type),
                        "value": payment.value,
                        "client_uuid": payment.client_uuid,
                        "callback_url": payment.callback_url,
                        "error_message": str(e),
                    }
                },
            )

            raise e