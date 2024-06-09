from fastapi import APIRouter

from kanbanize.schemas import (
    Group,
    GroupResponse,
    GroupUuid,
    Table,
    TableResponse,
    TableUuid,
)

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



