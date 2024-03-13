from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from kanbanize.main_api.schemas import (
    GroupResponse,
    TableResponse,
    TaskResponse,
)

app = FastAPI()


@app.get("/")
def read_root():
    return RedirectResponse("/docs/")


@app.post("/table")
def create_table() -> TableResponse:
    # Code to create a table goes here
    pass


@app.get("/table")
def get_table() -> TaskResponse:
    # Code to get a table goes here
    pass


@app.post("/group")
def create_group() -> GroupResponse:
    # Code to create a group goes here
    pass


@app.get("/group")
def get_group() -> GroupResponse:
    # Code to get a group goes here
    pass


@app.post("/group")
def create_task() -> TaskResponse:
    # Code to create a group goes here
    pass


@app.get("/group")
def get_task() -> TaskResponse:
    # Code to get a group goes here
    pass
