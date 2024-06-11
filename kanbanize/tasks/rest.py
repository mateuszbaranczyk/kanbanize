from fastapi import APIRouter, FastAPI, HTTPException

from kanbanize.firestore_adapter import DocumentError
from kanbanize.schemas import Task, TaskResponse, TaskUuid
from kanbanize.tasks import crud
from kanbanize.tasks.events import (  # noqa: F401
    TaskConnectedEvent,
    TaskDisconnectedEvent,
    handle_events,
)
from kanbanize.validation import validate

app = FastAPI()

task = APIRouter(prefix="/task")


@task.post("/create")
async def create(task: Task) -> TaskResponse:
    adapter = crud.TasksAdapter()
    try:
        result = adapter.create(data=task)
    except DocumentError:
        raise HTTPException(500)

    if task.table_uuid:
        TaskConnectedEvent(result).send()
    return result


@task.get("/get/{uuid}")
async def get(uuid: TaskUuid) -> TaskResponse:
    adapter = crud.TasksAdapter()
    try:
        task = adapter.get(uuid)
    except NameError:
        raise HTTPException(404)
    return task


@task.put("/edit/{uuid}")
async def edit(data: dict, uuid: TaskUuid) -> TaskResponse:
    validate(data)
    adapter = crud.TasksAdapter()
    try:
        result = adapter.edit(uuid, data)
    except NameError:
        raise HTTPException(404)
    handle_events(data, result)
    return task


app.include_router(task)
