from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from google.cloud import firestore

from kanbanize.firestore_adapter import DocumentError
from kanbanize.schemas import Task, TaskResponse, TaskUuid
from kanbanize.tasks import crud
from kanbanize.tasks.database import get_db
from kanbanize.tasks.events import (  # noqa: F401
    TaskConnectedEvent,
    TaskDisconnectedEvent,
    handle_events,
)
from kanbanize.validation import validate

app = FastAPI()

task = APIRouter(prefix="/task")


@app.get("/")
async def read_root():
    return RedirectResponse("docs/")


@task.post("/create")
async def create(
    task: Task, db: firestore.Client = Depends(get_db)
) -> TaskResponse:
    adapter = crud.TasksAdapter(db)
    try:
        result = adapter.create(data=task)
    except DocumentError:
        raise HTTPException(500)

    if task.table_uuid:
        TaskConnectedEvent(result).send()
    return result


@task.get("/get/{uuid}")
async def get(
    uuid: TaskUuid, db: firestore.Client = Depends(get_db)
) -> TaskResponse:
    adapter = crud.TasksAdapter(db)
    try:
        task = adapter.get(uuid)
    except NameError:
        raise HTTPException(404)
    return task


@task.put("/edit/{uuid}")
async def edit(
    data: dict, uuid: TaskUuid, db: firestore.Client = Depends(get_db)
) -> TaskResponse:
    validate(data)
    adapter = crud.TasksAdapter(db)
    try:
        result = adapter.edit(uuid, data)
    except NameError:
        raise HTTPException(404)
    handle_events(data, result)
    return result


app.include_router(task)
