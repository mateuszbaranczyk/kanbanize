from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from kanbanize.main_api.rest import table, task

rest = FastAPI()


rest.include_router(table)
rest.include_router(task)


@rest.get("/")
async def read_root():
    return RedirectResponse("/docs/")
