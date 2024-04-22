import pytest
from unittest import mock

from api.application_layer.use_cases.payment import PaymentUseCase
from api.domain_layer.models.payment import Payment
from api.presentation_layer.views.api import PaymentCreateMapping


def create_mapping(payload):
    return PaymentCreateMapping(payload=payload)

@mock.patch.object(Payment, 'create')
def test_create_payment(mock_create_payment):
    
    mapping = PaymentCreateMapping(payload={
        "type": 'Teste_ type',
        "value": 100.00,
        "client_uuit": 'Teste client_uuid',
        "callback_url": 'http://teste.com'
    })
    
    PaymentUseCase.create_payment(mapping)

    mock_create_payment.assert_called_once_with(
        type=mapping.type, 
        value=mapping.value,
        client_uuid=mapping.client_uuid,
        callback_url=mapping.callback_url
    )