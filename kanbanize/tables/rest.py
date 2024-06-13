from fastapi import APIRouter, Depends, FastAPI, HTTPException
from google.cloud import firestore

from kanbanize.firestore_adapter import DocumentError
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
    try:
        table = adapter.create(data=table)
    except DocumentError:
        raise HTTPException(500)
    return table


@table.get("/get/{uuid}")
async def get(uuid: TableUuid, db: firestore.Client = Depends(get_db)):
    adapter = crud.TablesAdapter(db)
    try:
        table = adapter.get(uuid)
    except NameError:
        raise HTTPException(404)
    return table


@table.put("/edit")
async def edit(db: firestore.Client = Depends(get_db)):
    pass


app.include_router(table)
