from fastapi import APIRouter, FastAPI

table = APIRouter(prefix="/table", tags=["table"])
task = APIRouter(prefix="/task", tags=["task"])
group = APIRouter(prefix="/group", tags=["group"])

app = FastAPI()
