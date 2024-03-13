from typing import NewType

from pydantic import BaseModel

Uuid = NewType("Uuid", str)


class Task(BaseModel):
    name: str
    status: str
    notes: str = ""


class TaskResponse(Task):
    uuid: Uuid


class Table(BaseModel):
    name: str
    tasks: list[TaskResponse] = []


class TableResponse(Table):
    uuid: Uuid


class Group(BaseModel):
    name: str
    project: str
    tables: list[TableResponse] = []


class GroupResponse(Group):
    uuid: Uuid
