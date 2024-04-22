from dataclasses import dataclass
from enum import Enum
from flask import current_app
from typing import Optional
from uuid import UUID, uuid4


class PaymentTypeEnum(Enum):
    PHYSICAL_PRODUCT='Produto físico'
    BOOK='Livro'
    MEMBER_ASSOCIATION='Associação de membro'
    ASSOCIATION_UPGRADE='Upgrade associação'
    VIDEO_APRENDENDO_ESQUIAR='Vídeo aprendendo esquiar'
    
class StatusEnum(Enum):
    WAITING='Waiting'
    PROCESSING='Processing'
    FINISHED='Finished'


@dataclass
class Stage:
    
    payment_uuid: UUID
    stage: str
    status: StatusEnum
        

@dataclass
class Payment:
    
    type: PaymentTypeEnum
    value: float
    client_uuid: UUID
    callback_url: str
    id: str = None
    
    @classmethod
    def create(
        cls, 
        type: PaymentTypeEnum, 
        value: float, 
        client_uuid: UUID,
        callback_url: str):
        from api.application_layer.adapter.payment_repository import PaymentsRepository
        
        new_payment = Payment(
            type = type,
            value = value,
            client_uuid = client_uuid,
            callback_url = callback_url
        )

        new_payment.id = PaymentsRepository.persist_payment(payment=new_payment)
        return new_payment
    
    def process(self):
        from api.application_layer.adapter.sqs_pubsub import MessageAnnouncerSQS
        
        MessageAnnouncerSQS.send_message(
            name=current_app.config['QUEUE_PROCESS_PAYMENTS'],
            message_body=self.to_json()
        )
        

    def to_json(self):
        return {
            'type': self.type,
            'value': self.value,
            'client_uuid': self.client_uuid,
            'callback_url': self.callback_url,
            'id': self.id
        }