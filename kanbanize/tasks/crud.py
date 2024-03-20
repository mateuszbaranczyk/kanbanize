from google.cloud import firestore

from kanbanize.data_structures.schemas import Task, TaskResponse
from kanbanize.tasks.database import DB_TIMEOUT, TASKS_COLLECTION


def create_task(db: firestore.Client, task: Task) -> TaskResponse:
    db_object = TaskResponse(**task.model_dump())
    task_dump = db_object.model_dump()

    db_document = db.collection(TASKS_COLLECTION).document(db_object.uuid)
    db_document.set(data=task_dump, timeout=DB_TIMEOUT)
    return db_object


# https://cloud.google.com/firestore/docs/manage-data/add-data
