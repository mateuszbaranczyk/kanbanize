from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class TaskDataValidator:
    name: str = ""
    status: str = ""
    notes: str = ""
    table_uuid: str = ""


def validate(data: dict) -> None:
    try:
        TaskDataValidator(**data)
    except TypeError:
        raise HTTPException(422)
