from fastapi import APIRouter, Depends, FastAPI, HTTPException
from google.cloud import firestore

from kanbanize.data_structures.schemas import Task, TaskResponse, TaskUuid
from kanbanize.tasks import crud
from kanbanize.tasks.database import get_db
from kanbanize.tasks.events import send_event

app = FastAPI()

task = APIRouter(prefix="/task")


@task.post("/create")
async def create_task(
    task: Task, db: firestore.Client = Depends(get_db)
) -> TaskResponse:
    result = crud.create_task(db, task)
    if result.table_uuid:
        send_event()
    return result

    # TODO
    # save event to db?


@task.get("/get/{uuid}")
def get_task(
    uuid: TaskUuid, db: firestore.Client = Depends(get_db)
) -> TaskResponse:
    try:
        task = crud.get_task(db, uuid)
        return task
    except NameError:
        raise HTTPException(404)


app.include_router(task)
