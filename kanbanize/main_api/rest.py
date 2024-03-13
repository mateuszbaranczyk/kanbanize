from fastapi.responses import RedirectResponse

from kanbanize.main_api.main import app, group, table, task
from kanbanize.main_api.schemas import (
    Group,
    GroupResponse,
    Table,
    TableResponse,
    Task,
    TaskResponse,
)


@app.get("/")
async def read_root():
    return RedirectResponse("/docs/")


@table.post("/create")
async def create_table(table: Table) -> TableResponse:
    #
    return "table"


@table.get("/get/{uuid}")
async def get_table(uuid) -> TableResponse:
    # Code to get a table goes here
    pass


@table.patch("/edit/{uuid}")
async def edit_table(uuid) -> Table:
    pass


@group.post("/create")
async def create_group(group: Group) -> GroupResponse:
    # Code to create a group goes here
    pass


@group.get("/get/{uuid}")
async def get_group(uuid) -> GroupResponse:
    # Code to get a group goes here
    return "group"


@group.patch("/edit/{uuid}")
async def edit_group(uuid) -> GroupResponse:
    pass


@task.post("/create")
async def create_task(task: Task) -> TaskResponse:
    # Code to create a group goes here
    pass


@task.get("/get/{uuid}")
async def get_task(uuid) -> TaskResponse:
    # Code to get a group goes here
    return "task"


@task.patch("/edit/{uuid}")
async def edit_task(uuid) -> TaskResponse:
    pass


app.include_router(table)
app.include_router(task)
app.include_router(group)
