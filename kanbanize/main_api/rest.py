from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def read_root():
    return RedirectResponse("/docs/")


@app.post("/table")
def create_table():
    # Code to create a table goes here
    pass


@app.get("/table")
def get_table():
    # Code to get a table goes here
    pass


@app.post("/group")
def create_group():
    # Code to create a group goes here
    pass


@app.get("/group")
def get_group():
    # Code to get a group goes here
    pass
