from fastapi import APIRouter, FastAPI

from kanbanize.data_structures.schemas import Task, TaskResponse

app = FastAPI()

task = APIRouter(prefix="/task")


@task.post("/create")
async def create_task(task: Task) -> TaskResponse:
    pass
    # TODO
    # save to db
    # send event created_task
    # save event to db
