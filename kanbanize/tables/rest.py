from fastapi import APIRouter, Depends, FastAPI
from google.cloud import firestore

from kanbanize.schemas import Table, TableResponse, TableUuid
from kanbanize.tables import crud
from kanbanize.tables.database import get_db

app = FastAPI()

table = APIRouter(prefix="/tables")


@table.post("/create")
async def create(
    table: Table, db: firestore.Client = Depends(get_db)
) -> TableResponse:
    adapter = crud.TablesAdapter(db)
    table = adapter.create(data=table)
    return table


@table.get("get")
async def get(uuid: TableUuid, db: firestore.Client = Depends(get_db)):
    pass


@table.put("/edit")
async def edit(db: firestore.Client = Depends(get_db)):
    pass


app.include_router(table)
