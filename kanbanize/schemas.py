from typing import NewType
from uuid import uuid4

from pydantic import BaseModel

TASK_PREFIX = "ta"
TABLE_PREFIX = "tb"

Uuid = NewType("Uuid", str)
TaskUuid = NewType("TaskUuid", Uuid)
GroupUuid = NewType("GroupUuid", Uuid)
TableUuid = NewType("TableUuid", Uuid)


def create_uuid(prefix: str) -> Uuid:
    uuid = str(uuid4())
    return f"{prefix}-{uuid}"


class Task(BaseModel):
    name: str
    status: str
    notes: str = ""

    table_uuid: TableUuid = ""


class TaskResponse(Task):
    uuid: TaskUuid = create_uuid(TASK_PREFIX)


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
