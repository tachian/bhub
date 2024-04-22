class PayloadMapping:
    def __init__(self, *, payload):
        self.payload = payload


class PaymentCreateMapping(PayloadMapping):

    @property
    def type(self):
        return self.payload.get('type')

    @property
    def value(self):
        return self.payload.get('value')
    
    @property
    def client_uuid(self):
        return self.payload.get('client_uuid')
    
    @property
    def callback_url(self):
        return self.payload.get('callback_url')
