import pytest
from unittest import mock

from api.application_layer.adapter.payment_repository import PaymentsRepository
from api.domain_layer.models.payment import Payment, PaymentTypeEnum

@mock.patch.object(PaymentsRepository, 'persist_payment')
def test_create(mock_persist_payment):
    
    mock_persist_payment.return_value = 'teste_id'

    payment = Payment.create(
        type=PaymentTypeEnum.ASSOCIATION_UPGRADE,
        value=100.0,
        client_uuid='teste uuid',
        callback_url='www.teste.com'
    )
    
    expected_payment = Payment(
        id='teste_id',
        type=PaymentTypeEnum.ASSOCIATION_UPGRADE,
        value=100.0,
        client_uuid='teste uuid',
        callback_url='www.teste.com'
    )
    assert payment == expected_payment