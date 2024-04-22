import pytest
from unittest import mock
from uuid import UUID, uuid4

from api.app import mongo_client
from api.application_layer.adapter.payment_repository import PaymentsRepository
from api.domain_layer.models.payment import Payment, PaymentTypeEnum

def _create_payment(type: PaymentTypeEnum, client_uuid: UUID):    
    return Payment(
        type=type,
        value=100.0,
        client_uuid=client_uuid,
        callback_url='http://test.com'
    )

def test_persist_payment(app):
    client_uuid = str(uuid4())
    PaymentsRepository.persist_payment(_create_payment(type=PaymentTypeEnum.ASSOCIATION_UPGRADE, client_uuid=client_uuid))
    inserted_payment = mongo_client.db.Payments.find_one()

    assert inserted_payment["type"] == PaymentTypeEnum.ASSOCIATION_UPGRADE.value
    assert inserted_payment["client_uuid"] == client_uuid


@mock.patch('api.application_layer.adapter.payment_repository.logger.exception')
@mock.patch('api.application_layer.adapter.payment_repository.mongo_client.db.Payments.insert_one')
def test_persist_payment_with_error(mock_mongo, mock_logger, app):
    client_uuid = str(uuid4())
    msg = 'Error persisting payment'
    mock_mongo.side_effect = Exception(msg)
    payment = _create_payment(type=PaymentTypeEnum.ASSOCIATION_UPGRADE, client_uuid=client_uuid)
    
    with pytest.raises(Exception,
                        match=msg):
        PaymentsRepository.persist_payment(payment=payment)    
    
    mock_logger.assert_called_once_with(msg, extra={
                    "props": {
                        "service": "PaymentsRepository",
                        "method": "persist_payment",
                        "type": str(payment.type),
                        "value": payment.value,
                        "client_uuid": payment.client_uuid,
                        "callback_url": payment.callback_url,
                        "error_message": str(msg),
                    }
                })