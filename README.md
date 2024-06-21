# Kanbanize

It's a simple rest API that communicates with two microservices. RabbitMQ is used for communication between services. Data are stored in Firebase.

I'm planning to:
- deploy the whole app in GCP
- create Docker for every component (API and services)
- complete functionalities 
- create front in Next.js as a separate project

# dev testing

run firebase emulator and copy addres 

`gcloud emulators firestore start`

export emulator addres for both task and tables

run services on its directories
 - main api `uvicorn run:rest --reload`
 - tasks `uvicorn rest:app --reload --port=8888` 
 - tables `uvicorn rest:app --reload --port=9999`
 
api should be avaliable under http://localhost:8000