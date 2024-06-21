from fastapi import APIRouter, Depends

from kanbanize.main_api.adapters import TableAdapter, TaskAdapter
from kanbanize.schemas import (
    Table,
    TableResponse,
    TableUuid,
    Task,
    TaskResponse,
    TaskUuid,
)

task = APIRouter(prefix="/task", tags=["task"])
table = APIRouter(prefix="/table", tags=["table"])


@table.post("/create")
async def create_table(
    table: Table,
    adapter: TableAdapter = Depends(TableAdapter),
) -> TableResponse:
    data = table.model_dump_json()
    response = adapter.create(data)
    return response


@table.get("/get/{uuid}")
async def get_table(
    uuid: TableUuid,
    adapter: TableAdapter = Depends(TableAdapter),
) -> TableResponse:
    return adapter.get(uuid)


@table.put("/edit/{uuid}")
async def edit_table(
    uuid: TableUuid,
    table: Table,
    adapter: TableAdapter = Depends(TableAdapter),
) -> TableResponse:
    data = table.model_dump_json()
    return adapter.edit(uuid, data)


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
