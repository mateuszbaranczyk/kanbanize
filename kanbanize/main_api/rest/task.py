from fastapi import APIRouter, Depends

from kanbanize.main_api.adapters import TaskAdapter
from kanbanize.schemas import (
    Task,
    TaskResponse,
    TaskUuid,
)

task = APIRouter(prefix="/task", tags=["task"])


@task.post("/create")
async def create_task(
    task: Task, adapter: TaskAdapter = Depends(TaskAdapter)
) -> TaskResponse:
    task_data = task.model_dump_json()
    return adapter.create(task_data)


@task.get("/get/{uuid}")
async def get_task(
    uuid: TaskUuid, adapter: TaskAdapter = Depends(TaskAdapter)
) -> TaskResponse:
    return adapter.get(uuid)


@task.put("/edit/{uuid}")
async def edit_task(
    uuid: TaskUuid,
    task_data: dict,
    adapter: TaskAdapter = Depends(TaskAdapter),
) -> TaskResponse:
    return adapter.edit(uuid, task_data)
