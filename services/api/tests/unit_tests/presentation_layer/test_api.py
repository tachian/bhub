import pytest
from unittest import mock

from api.application_layer.use_cases.payment import PaymentUseCase
from api.domain_layer.models.payment import PaymentTypeEnum, Payment


def test_health(app):
    result = app.get("/health")

    assert result.json == {"service": "API Bhub HealthCheck", "version": "1.0"}

@mock.patch.object(PaymentUseCase, 'create_payment')
def test_create_paymet(mock_create_payment, app):
    
    expected_payment = Payment(
        id='Teste ID',
        type=PaymentTypeEnum.BOOK.value,
        value="01234567891",
        client_uuid="",
        callback_url="John Doe")
    mock_create_payment.return_value = expected_payment
    
    request_json = {
        "type": PaymentTypeEnum.BOOK.value,
        "value": 100.0,
        "client_uuid": "",
        "callback_url": "John Doe"
    }
    
    response = app.post("/payment", json=request_json)
    
    assert response.status == '201 CREATED'
    assert response.json == {"message": f"Payment {expected_payment.id} created successfully"}
    assert mock_create_payment.call_args.kwargs["data"].payload == request_json
    
def test_create_paymet_with_invalid_payload(app):
    
    request_json = {
        "type": 99,
        "value": 100.0,
        "client_uuid": "",
        "callback_url": "John Doe"
    }
    
    response = app.post("/payment", json=request_json)

    assert response.status == '400 BAD REQUEST'
    assert response.json['message'] == 'Input payload validation failed'
    assert response.json['errors'] == {'type': "99 is not one of ('Upgrade associação', 'Livro', 'Associação de membro', 'Produto físico', 'Vídeo aprendendo esquiar')"}

@mock.patch('api.presentation_layer.views.api.logger.exception')
@mock.patch.object(PaymentUseCase, 'create_payment')
def test_create_paymet_with_exception_on_usecase(mock_create_payment, mock_logger, app):
    
    msg = 'Erro ao executar usecase'
    mock_create_payment.side_effect = Exception(msg)
    
    request_json = {
        "type": PaymentTypeEnum.BOOK.value,
        "value": 100.0,
        "client_uuid": "",
        "callback_url": "John Doe"
    }
    
    response = app.post("/payment", json=request_json)

    assert response.status == '500 INTERNAL SERVER ERROR'
    assert response.json['message'] == 'Error on create payment'
    mock_logger.assert_called_once_with(
        'Failed to create Client', 
        extra={
            "props": {
                "request": "/clients/",
                "method": "POST",
                "type": request_json['type'],
                "value": request_json['value'],
                "cliente_uuid": request_json['client_uuid'],
                "callback_url": request_json['callback_url'],
                "error_message": msg
            }
        }
    )
