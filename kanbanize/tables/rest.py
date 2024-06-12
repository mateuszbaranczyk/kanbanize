from fastapi import APIRouter, Depends, FastAPI
from google.cloud import firestore

from kanbanize.tables.database import get_db

app = FastAPI()

task = APIRouter(prefix="/tables")


@task.post("/create")
async def create(db: firestore.Client = Depends(get_db)):
    pass


@task.post("get(")
async def get(db: firestore.Client = Depends(get_db)):
    pass


@task.post("/edit")
async def edit(db: firestore.Client = Depends(get_db)):
    pass
