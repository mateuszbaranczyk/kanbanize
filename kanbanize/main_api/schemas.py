from pydantic import BaseModel


class Task(BaseModel):
    name: str
    status: str
    notes: str


class Table(BaseModel):
    name: str
    tasks: list[Task] = []


class Group(BaseModel):
    name: str
    project: str
    tables: list[Table] = []


class TaskResponse(Task):
    uuid: str


class GroupResponse(Group):
    uuid: str


class TableResponse(Table):
    uuid: str
