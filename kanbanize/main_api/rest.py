from fastapi import APIRouter

from kanbanize.main_api.schemas import (
    Group,
    GroupResponse,
    Table,
    TableResponse,
    Task,
    TaskResponse,
    Uuid,
)

table = APIRouter(prefix="/table", tags=["table"])
task = APIRouter(prefix="/task", tags=["task"])
group = APIRouter(prefix="/group", tags=["group"])


@table.post("/create")
async def create_table(table: Table) -> TableResponse:
    result = TableResponse(name=table.name, tasks=table.tasks, uuid="uuid123")
    return result


@table.get("/get/{uuid}")
async def get_table(uuid: Uuid) -> TableResponse:
    t1 = TaskResponse(name="test1", status="done", notes="", uuid="uuid1")
    t2 = TaskResponse(name="test2", status="done", notes="", uuid="uuid2")
    result = TableResponse(name="table name", tasks=[t1, t2], uuid=uuid)
    return result


@table.patch("/edit/{uuid}")
async def edit_table(uuid: Uuid) -> Table:
    pass


@group.post("/create")
async def create_group(group: Group) -> GroupResponse:
    # Code to create a group goes here
    pass


@group.get("/get/{uuid}")
async def get_group(uuid: Uuid) -> GroupResponse:
    # Code to get a group goes here
    return "group"


@group.patch("/edit/{uuid}")
async def edit_group(uuid: Uuid) -> GroupResponse:
    pass


@task.post("/create")
async def create_task(task: Task) -> TaskResponse:
    result = TaskResponse(
        name=task.name, status=task.status, notes=task.notes, uuid="dfa21-2313"
    )
    return result


@task.get("/get/{uuid}")
async def get_task(uuid: Uuid) -> TaskResponse:
    result = TaskResponse(name="test", status="done", notes="", uuid=uuid)
    return result


@task.patch("/edit/{uuid}")
async def edit_task(uuid: Uuid) -> TaskResponse:
    pass
