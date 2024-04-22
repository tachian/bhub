from api.domain_layer.models.payment import Payment
from api.presentation_layer.views.mapping import PaymentCreateMapping

class PaymentUseCase:
    
    @classmethod
    def create_payment(cls, data: PaymentCreateMapping):
        
        return Payment.create(
            type=data.type, 
            value=data.value,
            client_uuid=data.client_uuid,
            callback_url=data.callback_url)
