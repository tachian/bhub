
import json
import boto3
import redis
import os
import logging
from enum import Enum
from pymongo import MongoClient


log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = MongoClient(host=os.environ.get("ATLAS_URI"))
db = client.BHUB
collection = db.Payments

sqs = boto3.client('sqs')

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

def lambda_handler(event, context):
    
    try:
        for message in event['Records']:
            payment = set_events(message)
            process_payment(payment)
            
            log.info(
                "Start process payment",
                extra={
                    "props": {
                        "method": "lambda_handler",
                        "id": str(payment.id),
                    }
                }
             )
            
        return {
            'statusCode': 200,
            'body': json.dumps(message)
        } 

    except Exception as ex:
        log.debug("failed to connect to redis:", ex.__class__, " occurred")
        return {
            'statusCode': 500
        }
    finally:
        del redis_conn

def set_events(message):
    try:
        payment = collection.find_one(message['body']['id'])
        log.info(
            "Payment created",
            extra={
                "props": {
                    "method": "Creating Events",
                    "id": str(payment.id),
                }
            }
        )
        
        redis_conn = connect_redis()
        config_payment = redis_conn.get(f"#Payment#{payment.client_uuid}")
        
        payment['events'] = config_payment[payment.type]
        
        myquery = { "_id": payment.id }
        newvalues = { "$set": { "events": payment['events'] } }
        collection.update_one(myquery, newvalues)
        
        return payment 

    except Exception as err:
        print("An error occurred")
        raise err
    

def process_payment(payment):
    
    for payment_type in payment['events']:
        sqs = boto3.client('sqs')

        sqs.send_message(
            QueueUrl=f"https://sqs.us-west-1.amazonaws.com/340928755085/{payment_type}",
            MessageBody=payment
        )
      
def connect_redis():

    redis_endpoint = None
    redis_port = None
    redis_auth = None
    if "REDIS_HOST" in os.environ and "REDIS_AUTH" in os.environ and "REDIS_PORT" in os.environ:
        redis_endpoint = os.environ["REDIS_HOST"]
        redis_port = os.environ["REDIS_PORT"]
        redis_auth = os.environ["REDIS_AUTH"]
        log.debug("redis: " + redis_endpoint)
    else:
        raise "REDIS_HOST REDIS_PORT REDIS_AUTH configuration not set !"
    
    return redis.StrictRedis(host=redis_endpoint, port=redis_port, db=0, ssl=True, password=redis_auth)  

# {
#     "#Payment#UUID-11111-22222-33333":{
#         'Produto físico': ["gerar-guia-remessa-arquivo", "gerar-pagamento-comissao-agente"],
#         'Livro': ["gerar-guia-remessa-duplicada-departamento-royalties", "gerar-pagamento-comissao-agente"],
#         'Associação de membro': ["ativar-associacao", "enviar-email-notificando-ativacao-upgrade"],
#         'Upgrade associação': ["aplicar-upgrade", "enviar-email-notificando-ativacao-upgrade"],
#         'Video aprendendo esquiar': ["adicionar-video-primeiros-socorros"]
#     },
#     "#Payment#UUID-11111-22222-33333":{
#         'Produto físico': ["gerar-guia-remessa-arquivo", "gerar-pagamento-comissao-agente"],
#         'Livro': ["gerar-guia-remessa-duplicada-departamento-royalties", "gerar-pagamento-comissao-agente"],
#         'Associação de membro': ["ativar-associacao", "enviar-email-notificando-ativacao-upgrade"],
#         'Upgrade associação': ["aplcar-upgrade", "enviar-email-notificando-ativacao-upgrade"],
#         'Video aprendendo esquiar': ["adicionar-video-primeiros-socorros"]
#     },
# }

