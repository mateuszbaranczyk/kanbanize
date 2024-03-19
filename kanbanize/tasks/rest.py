import crud
from database import get_db
from fastapi import APIRouter, Depends, FastAPI
from google.cloud import firestore

from kanbanize.data_structures.schemas import Task, TaskResponse

app = FastAPI()

task = APIRouter(prefix="/task")


@task.post("/create")
async def create_task(
    task: Task, db: firestore.Client = Depends(get_db)
) -> TaskResponse:
    result = crud.create_task(db, task)
    return result

    # TODO
    # send event created_task
    # save event to db?
