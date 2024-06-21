# Kanbanize

It's a simple rest API that communicates with two microservices. RabbitMQ is used for communication between services. Data is stored in Firebase.

DONE:
- rest api's for all components
- firebase connection
- events on tasks side

TO DO:
- event handling on table side
- docker compose 

# dev testing

run firebase emulator and copy addres 

`gcloud emulators firestore start --host-port=127.0.0.1:8328`

set env variable emulator addres for both task and tables

`export FIRESTORE_EMULATOR_HOST=127.0.0.1:8328`

run services on its directories
 - main api `uvicorn run:rest --reload`
 - tasks `uvicorn rest:app --reload --port=8888` 
 - tables `uvicorn rest:app --reload --port=9999`
 
api should be avaliable under http://localhost:8000