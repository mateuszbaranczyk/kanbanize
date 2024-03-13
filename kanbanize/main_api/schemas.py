from pydantic import BaseModel


class Task(BaseModel):
    name: str
    status: str
    notes: str


class Table(BaseModel):
    name: str
    tasks: Task


class Group(BaseModel):
    name: str
    tables: Table
