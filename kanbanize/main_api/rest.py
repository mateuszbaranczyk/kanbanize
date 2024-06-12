from fastapi import APIRouter, Depends

from kanbanize.main_api.adapters import TaskAdapter
from kanbanize.schemas import (
    Group,
    GroupResponse,
    GroupUuid,
    Table,
    TableResponse,
    TableUuid,
    Task,
    TaskResponse,
    TaskUuid,
)

task = APIRouter(prefix="/task", tags=["task"])
table = APIRouter(prefix="/table", tags=["table"])
group = APIRouter(prefix="/group", tags=["group"])


@table.post("/create")
async def create_table(table: Table) -> TableResponse:
    return table


@table.get("/get/{uuid}")
async def get_table(uuid: TableUuid) -> TableResponse:
    return uuid


@table.put("/edit/{uuid}")
async def edit_table(uuid: TableUuid, table: Table) -> TableResponse:
    return table


@group.post("/create")
async def create_group(group: Group) -> GroupResponse:
    return group


@group.get("/get/{uuid}")
async def get_group(uuid: GroupUuid) -> GroupResponse:
    return uuid


@group.put("/edit/{uuid}")
async def edit_group(uuid: GroupUuid, group: Group) -> GroupResponse:
    return group


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
