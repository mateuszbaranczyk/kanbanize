from google.cloud import firestore

from kanbanize.data_structures.schemas import Task, TaskResponse
from kanbanize.tasks.database import DB_TIMEOUT, TASKS_COLLECTION


def create_task(db: firestore.Client, task: Task) -> TaskResponse:
    data = TaskResponse(**task)
    task_dump = data.model_dump()

    db_document = db.collection(TASKS_COLLECTION).document(data.uuid)
    db_document.set(task_dump, timeout=DB_TIMEOUT)
    return data


# https://cloud.google.com/firestore/docs/manage-data/add-data
