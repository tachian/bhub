# Bhuh - Services

## Service to create payment
### Dependencies
 + [MongoDB](https://www.mongodb.com/docs/manual/installation/)

### Class Diagram
   + [Sequence Diagram](https://sequencediagram.org/)
   + Copy and Paste code below on Sequence Diagram
```
title Bhub - Payment Process
actor Cliente
participant API
participant FILA
participant Lambda
participant Redis
participant Worker
Cliente->API: Efetua requisição do serviço que será excutado
API->FILA:Cria item na fila para que seja processamento
FILA->(1)Lambda: Inicia o processamento da requisição
Lambda->Redis: Solicita configuração
Redis->Lambda: Retorna JSON com configuração
Lambda-> FILA: Solicita o processamento
FILA->WORKER: Efetua o processamento
WORKER->FILA: Solicita Atualização do Status Processamento
FILA->WORKER: Atualiza Status 
WORKER->Cliente: Notifica Término Processmento
```
