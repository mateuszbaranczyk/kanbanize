from google.cloud import firestore

from kanbanize.firestore_adapter import FirestoreAdapter
from kanbanize.schemas import Task, TaskResponse, TaskUuid
from kanbanize.tasks import database


class TasksCRUD(FirestoreAdapter):
    db = database.get_db()
    model = Task
    response_model = TaskResponse
    COLLECTION = database.COLLECTION


def create(db: firestore.Client, task: Task) -> TaskResponse:
    db_object = TaskResponse(**task.model_dump())
    task_dump = db_object.model_dump()

    created_document = _save_and_get(db, db_object, task_dump)
    return TaskResponse(**created_document)


def _save_and_get(db, db_object: TaskResponse, task_dump: dict) -> dict:
    db_document = db.collection(database.COLLECTION).document(db_object.uuid)
    db_document.set(task_dump, timeout=database.DB_TIMEOUT)
    created_document = (
        db.collection(database.COLLECTION).document(db_object.uuid).get()
    ).to_dict()

    return created_document


def get(db: firestore.Client, uuid: TaskUuid) -> TaskResponse:
    db_document = db.collection(database.COLLECTION).document(uuid)
    task = db_document.get()

    if task.exists:
        return TaskResponse(**task.to_dict())
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


def _edit_and_get(db, uuid: TaskUuid, task_data: dict) -> dict:
    db_document = db.collection(database.COLLECTION).document(uuid)
    db_document.update(task_data, timeout=database.DB_TIMEOUT)
    edited_document = (
        db.collection(database.COLLECTION).document(uuid).get()
    ).to_dict()

    return edited_document
