from fastapi import APIRouter

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
async def create_task(task: Task) -> TaskResponse:
    adapter = TaskAdapter()
    task_response = adapter.create(task.model_dump_json())
    return task_response


@task.get("/get/{uuid}")
async def get_task(uuid: TaskUuid) -> TaskResponse:
    return uuid


@task.put("/edit/{uuid}")
async def edit_task(uuid: TaskUuid, task: Task) -> TaskResponse:
    return task
