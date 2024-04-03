import os
from abc import ABC, abstractmethod

from requests import request

from kanbanize.schemas import (
    Group,
    GroupResponse,
    GroupUuid,
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
        result = request.get(url)
        return result.json

    @abstractmethod
    def edit(self, uuid: Uuid, object_: dict, endpoint="edit") -> dict:
        path = self.path(endpoint)
        url = f"{path}/{endpoint}/{uuid}"
        result = request("PUT", url=url, data=str(object_))
        return result.json()


class TaskAdapter(IAdapter):
    location = os.getenv("ADAPTER_LOCATION", "localhost:2020/task")

    def create(self, object_: Task.dict) -> TaskResponse:
        response = super().create(object_)
        return TaskResponse(**response)

    def get(self, uuid: TaskUuid) -> TaskResponse:
        response = super().get(uuid)
        return TaskResponse(**response)

    def edit(self, uuid: TaskUuid, object_: Task.dict) -> TaskResponse:
        response = super().edit(uuid, object_)
        return TaskResponse(**response)


class GroupAdapter(IAdapter):
    location = "localhost"

    def create(self, object_: Group.dict) -> GroupResponse:
        return super().create(object_)

    def get(self, uuid: GroupUuid) -> GroupResponse:
        return super().get(uuid)

    def edit(self, uuid: GroupUuid, object_: Group.dict) -> GroupResponse:
        return super().edit(uuid, object_)


class TableAdapter(IAdapter):
    location = "localhost"

    def create(self, object_: Table.dict) -> TableResponse:
        return super().create(object_)

    def get(self, uuid: TableUuid) -> TableResponse:
        return super().get(uuid)

    def edit(self, uuid: TableUuid, object_: Table.dict) -> TableResponse:
        return super().edit(uuid, object_)
