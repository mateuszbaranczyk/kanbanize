from typing import NewType

from pydantic import BaseModel

Uuid = NewType("Uuid", str)
TaskUuid = NewType("TaskUuid", Uuid)
GroupUuid = NewType("GroupUuid", Uuid)
TableUuid = NewType("TableUuid", Uuid)


class Task(BaseModel):
    name: str
    status: str
    notes: str = ""

    table_uuid: TableUuid = ""


class TaskResponse(Task):
    uuid: TaskUuid


class Table(BaseModel):
    name: str
    tasks: list[TaskResponse] = []

    group_uuid: GroupUuid = ""


class TableResponse(Table):
    uuid: TableUuid


class Group(BaseModel):
    name: str
    project: str
    tables: list[TableUuid] = []


class GroupResponse(Group):
    uuid: GroupUuid
