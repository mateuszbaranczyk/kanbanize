from fastapi import APIRouter, Depends, FastAPI
from google.cloud import firestore

from kanbanize.data_structures.schemas import Task, TaskResponse
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


app.include_router(task)
