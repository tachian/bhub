from flask_restx import fields, Model

from api.domain_layer.models.payment import PaymentTypeEnum


create_payment_model = Model(
    'create_payment', {
    'type': fields.String(required=True, enum=(
        PaymentTypeEnum.ASSOCIATION_UPGRADE.value,
        PaymentTypeEnum.BOOK.value,
        PaymentTypeEnum.MEMBER_ASSOCIATION.value,
        PaymentTypeEnum.PHYSICAL_PRODUCT.value,
        PaymentTypeEnum.VIDEO_APRENDENDO_ESQUIAR.value)),
    'value': fields.Float,
    'client_uuid': fields.String,
    'callback_url': fields.String
    })

