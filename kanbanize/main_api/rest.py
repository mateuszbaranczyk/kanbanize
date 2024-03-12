from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def read_root():
    return RedirectResponse("/hello/")


@app.get("/hello/")
def hello():
    return "Hello"
