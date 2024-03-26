from dataclasses import dataclass

from fastapi import HTTPException


@dataclass(frozen=True)
class TaskDataValidator:
    name: str = ""
    status: str = ""
    notes: str = ""
    table_uuid: str = ""


def validate(data: dict, validator: TaskDataValidator | None) -> None:
    try:
        validator(**data)
    except TypeError:
        raise HTTPException(422)
