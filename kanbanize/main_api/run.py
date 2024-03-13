from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from kanbanize.main_api.rest import group, table, task

app = FastAPI()


app.include_router(table)
app.include_router(task)
app.include_router(group)


@app.get("/")
async def read_root():
    return RedirectResponse("/docs/")
