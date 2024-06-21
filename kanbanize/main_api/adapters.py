import os
from abc import ABC, abstractmethod

from requests import request

from kanbanize.schemas import (
    Table,
    TableResponse,
    TableUuid,
    Task,
    TaskResponse,
    TaskUuid,
    Uuid,
)


class IAdapter(ABC):
    location: str

    def path(self, endpoint: str) -> str:
        path = f"http://{self.location}/{endpoint}"
        return path

    @abstractmethod
    def create(self, object_: dict, endpoint="create") -> dict:
        path = self.path(endpoint)
        result = request("POST", url=path, data=str(object_))
        return result.json()

    @abstractmethod
    def get(self, uuid: Uuid, endpoint="get") -> dict:
        path = self.path(endpoint)
        url = f"{path}/{uuid}/"
        result = request("GET", url=url)
        return result.json()

    @abstractmethod
    def edit(self, uuid: Uuid, object_: dict, endpoint="edit") -> dict:
        path = self.path(endpoint)
        url = f"{path}/{endpoint}/{uuid}"
        result = request("PUT", url=url, data=str(object_))
        return result.json()


class TaskAdapter(IAdapter):
    location = os.getenv("TASK_URL", "localhost:8888/task")

    def create(self, object_: Task.dict) -> TaskResponse:
        response = super().create(object_)
        return TaskResponse(**response)

    def get(self, uuid: TaskUuid) -> TaskResponse:
        response = super().get(uuid)
        return TaskResponse(**response)

    def edit(self, uuid: TaskUuid, object_: Task.dict) -> TaskResponse:
        response = super().edit(uuid, object_)
        return TaskResponse(**response)


class TableAdapter(IAdapter):
    location = os.getenv("TABLE_URL", "localhost:9999/table")

    def create(self, object_: Table.dict) -> TableResponse:
        response = super().create(object_)
        return TableResponse(**response)

    def get(self, uuid: TableUuid) -> TableResponse:
        response = super().get(uuid)
        return TableResponse(**response)

    def edit(self, uuid: TableUuid, object_: Table.dict) -> TableResponse:
        response = super().edit(uuid, object_)
        return TableResponse(**response)
