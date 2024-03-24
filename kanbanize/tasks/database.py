import os

from google.cloud import firestore

DB_TIMEOUT = 500.0
COLLECTION = "tasks"

project_id = os.getenv("PROJECT_ID")
database_name = os.getenv("DB_NAME", "kanbanize")


def get_db() -> firestore.Client:
    db = firestore.Client(project=project_id, database=database_name)
    yield db
