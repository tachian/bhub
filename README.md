# Bhuh - Services

## Service to create payment

 + Dependencies
   [MongoDB](https://www.mongodb.com/docs/manual/installation/)

 + Class Diagram
   + [Sequence Diagram](https://sequencediagram.org/)
   + ```
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

 + Start server (inside src dir)
    + `flask run`

 + HEALTH endpoints
    + /health: If API is working, must show {"service": "API Bhub HealthCheck", "version": "9.9.9"}

