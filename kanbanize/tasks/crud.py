from google.cloud import firestore

from kanbanize.schemas import Task, TaskResponse, TaskUuid
from kanbanize.tasks.database import COLLECTION, DB_TIMEOUT


def create(db: firestore.Client, task: Task) -> TaskResponse:
    db_object = TaskResponse(**task.model_dump())
    task_dump = db_object.model_dump()

    created_document = _save_and_get(db, db_object, task_dump)
    return TaskResponse(**created_document)


def _save_and_get(db, db_object, task_dump):
    db_document = db.collection(COLLECTION).document(db_object.uuid)
    db_document.set(data=task_dump, timeout=DB_TIMEOUT)
    created_document = (
        db.collection(COLLECTION).document(db_object.uuid).get()
    )._doc

    return created_document


def get(db: firestore.Client, uuid: TaskUuid) -> TaskResponse:
    db_document = db.collection(COLLECTION).document(uuid)
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

    edited_document = _edit_and_get(db, uuid, task_data)
    return TaskResponse(**edited_document)


def _edit_and_get(db, uuid, task_data):
    db_document = db.collection(COLLECTION).document(uuid)
    db_document.update(data=task_data, timeout=DB_TIMEOUT)
    edited_document = (db.collection(COLLECTION).document(uuid).get())._doc

    return edited_document
