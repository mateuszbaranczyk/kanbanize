from dataclasses import dataclass

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from google.cloud import firestore

from kanbanize.data_structures.schemas import Task, TaskResponse, TaskUuid
from kanbanize.tasks import crud
from kanbanize.tasks.database import get_db
from kanbanize.tasks.events import send_event

app = FastAPI()

task = APIRouter(prefix="/task")


@task.post("/create")
async def create(
    task: Task, db: firestore.Client = Depends(get_db)
) -> TaskResponse:
    result = crud.create(db, task)
    if result.table_uuid:
        send_event()
    return result

    # TODO
    # save event to db?


@task.get("/get/{uuid}")
def get(
    uuid: TaskUuid, db: firestore.Client = Depends(get_db)
) -> TaskResponse:
    try:
        task = crud.get(db, uuid)
        return task
    except NameError:
        raise HTTPException(404)


@dataclass
class TaskDataValidator:
    name: str = ""
    status: str = ""
    notes: str = ""
    table_uuid: str = ""


def validate(data):
    try:
        TaskDataValidator(**data)
    except TypeError:
        raise HTTPException(422)


def send_message(task, table_uuid):
    if table_uuid:
        send_event(task)


@task.put("/edit/{uuid}")
def edit(
    data: dict, uuid: TaskUuid, db: firestore.Client = Depends(get_db)
) -> TaskResponse:
    validate(data)
    table_uuid = data.get("table_uuid", None)

    try:
        task = crud.edit(db, uuid, data)
        send_message(task, table_uuid)
        return task
    except NameError:
        raise HTTPException(404)


app.include_router(task)
