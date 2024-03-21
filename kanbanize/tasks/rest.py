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


@task.put("/edit/{uuid}")
def edit(
    data: dict, uuid: TaskUuid, db: firestore.Client = Depends(get_db)
) -> TaskResponse:
    data = _validate_data(data)
    table_uuid = data.get("table_uuid", None)

    if table_uuid:
        send_event()

    return edit(db, uuid, data)


def _validate_data(data):
    for key, _ in data.items():
        if hasattr(Task, key):
            pass
        else:
            del data[key]
    return data


app.include_router(task)
