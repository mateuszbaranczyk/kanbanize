from google.cloud import firestore

from kanbanize.data_structures.schemas import Task, TaskResponse, TaskUuid
from kanbanize.tasks.database import DB_TIMEOUT, TASKS_COLLECTION


def create(db: firestore.Client, task: Task) -> TaskResponse:
    db_object = TaskResponse(**task.model_dump())
    task_dump = db_object.model_dump()

    db_document = db.collection(TASKS_COLLECTION).document(db_object.uuid)
    db_document.set(data=task_dump, timeout=DB_TIMEOUT)
    created_document = (
        db.collection(TASKS_COLLECTION).document(db_object.uuid).get()
    )._doc
    return TaskResponse(**created_document)


def get(db: firestore.Client, uuid: TaskUuid) -> TaskResponse:
    db_document = db.collection(TASKS_COLLECTION).document(uuid)
    task = db_document.get()
    if task.exists:
        return TaskResponse(**task._doc)
    else:
        raise NameError(f"No such document! {uuid}")


def edit(db: firestore.Client, uuid: TaskUuid, data: dict) -> TaskResponse:
    task = get(db, uuid)

    task_data = task.model_dump()
    for key, value in data.items():
        if key in task_data:
            task_data[key] = value

    db_document = db.collection(TASKS_COLLECTION).document(uuid)
    db_document.update(data=task_data, timeout=DB_TIMEOUT)
    edited_document = (
        db.collection(TASKS_COLLECTION).document(uuid).get()
    )._doc
    return TaskResponse(**edited_document)
