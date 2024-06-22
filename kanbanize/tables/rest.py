from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from google.cloud import firestore

from kanbanize.firestore_adapter import DocumentError
from kanbanize.schemas import Table, TableResponse, TableUuid
from kanbanize.tables import crud
from kanbanize.tables.database import get_db
from kanbanize.tables.listener import RabbitWorker

app = FastAPI()

table = APIRouter(prefix="/table")


@app.on_event("startup")
async def run_rabbit() -> None:
    RabbitWorker()
    return None


@app.get("/")
async def read_root():
    return RedirectResponse("docs/")


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


@table.put("/edit/{uuid}")
async def edit(
    uuid: TableUuid, data: dict, db: firestore.Client = Depends(get_db)
):
    adapter = crud.TablesAdapter(db)
    try:
        updated_table = adapter.edit(uuid, data)
    except DocumentError:
        raise HTTPException(500)
    except NameError:
        raise HTTPException(404)
    return updated_table


app.include_router(table)
