import json
from queue_client import sqs_client, QUEUE_URL


# a simple function that prints whatever message we give it
def display_message(message):
    print(f'your message is: {message}')


# a simple function that takes the sum of two values
def add_values(value_1, value_2):
    print(f'your sum is {value_1 + value_2}')

# this function converts the function name into python function object inside the global scope of this file/module
# there are other ways to do it but this is the simplest I can think of to run function based on its name
def execute_function_by_name(func_name, *args, **kwargs):
    if func_name in globals() and callable(globals()[func_name]):
        print(func_name)
        return globals()[func_name](*args, **kwargs)
    else:
        return f"No function named '{func_name}' found."

# this function will fetch data from queue and execution the function with given parameters
def worker():
    # infinte loop to keep on fetching from queue and process it
    while True:
        # fetch messages
        process("gerar-guia-remessa-arquivo" )
        process("gerar-pagamento-comissao-agente")
        process("gerar-guia-remessa-duplicada-departamento-royalties")
        process("ativar-associacao")
        process("enviar-email-notificando-ativacao-upgrade")
        process("aplcar-upgrade")
        process("enviar-email-notificando-ativacao-upgrade")
        process("adicionar-video-primeiros-socorros")

def process(queue_url: str):
    response = sqs_client.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=10,  # adjust as needed
        WaitTimeSeconds=10,  # adjust as needed
        MessageAttributeNames=['All'],
    )
    
    # process each message
    for message in response.get('Messages', []):
        print(f"\r\nReceived message: function: {message['Body']} :: parameters: {message['MessageAttributes']}")
        
        # get the function name
        function_name = message['MessageAttributes']['function']['StringValue']
        kwargs = json.loads(message['MessageAttributes']['kwargs']['StringValue'])
        print(function_name)
        print(kwargs)
        execute_function_by_name(function_name, **kwargs)
        sqs_client.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=message['ReceiptHandle']
        )
    else:
        print("No messages to process.")
    


if __name__ == "__main__":
    worker()