from fastapi import APIRouter, Depends, FastAPI, HTTPException
from google.cloud import firestore

from kanbanize.schemas import Task, TaskResponse, TaskUuid
from kanbanize.tasks import crud
from kanbanize.tasks.database import get_db
from kanbanize.tasks.events import TaskConnectedEvent, handle_events
from kanbanize.validation import validate

app = FastAPI()

task = APIRouter(prefix="/task")


@task.post("/create")
async def create(
    task: Task, db: firestore.Client = Depends(get_db)
) -> TaskResponse:
    result = crud.create(db, task)
    if task.table_uuid:
        TaskConnectedEvent(task).send()
    return result


@task.get("/get/{uuid}")
def get(
    uuid: TaskUuid, db: firestore.Client = Depends(get_db)
) -> TaskResponse:
    try:
        task = crud.get(db, uuid)
    except NameError:
        raise HTTPException(404)
    return task


@task.put("/edit/{uuid}")
def edit(
    data: dict, uuid: TaskUuid, db: firestore.Client = Depends(get_db)
) -> TaskResponse:
    validate(data)
    try:
        task = crud.edit(db, uuid, data)
    except NameError:
        raise HTTPException(404)
    handle_events(data, task)
    return task


app.include_router(task)
