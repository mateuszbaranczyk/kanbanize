from fastapi import APIRouter

from kanbanize.schemas import Table, TableResponse, TableUuid

table = APIRouter(prefix="/table", tags=["table"])


@table.post("/create")
async def create_table(table: Table) -> TableResponse:
    return table


@table.get("/get/{uuid}")
async def get_table(uuid: TableUuid) -> TableResponse:
    return uuid


@table.put("/edit/{uuid}")
async def edit_table(uuid: TableUuid, table: Table) -> TableResponse:
    return table
