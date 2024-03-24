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

    @abstractmethod
    def path(self, endpoint: str):
        path = f"http://{self.location}/{endpoint}"
        return path

    @abstractmethod
    def create(self, object_: dict, endpoint="create"):
        path = self.path(endpoint)
        result = request.post(path, object_)
        return result

    @abstractmethod
    def get(self, uuid: Uuid, endpoint="get"):
        path = self.path(endpoint)
        url = f"{path}/{uuid}/"
        result = request.get(url)
        return result

    @abstractmethod
    def edit(self, uuid: Uuid, object_: dict, endpoint="edit"):
        path = self.path(endpoint)
        url = f"{path}/{endpoint}/{uuid}"
        result = request.patch(url, object_)
        return result


class TaskAdapter(IAdapter):
    location = "localhost"

    def create(self, object_: Task.dict) -> TaskResponse:
        return super().create(object_)

    def get(self, uuid: TaskUuid) -> TaskResponse:
        return super().get(uuid)

    def edit(self, uuid: TaskUuid, object_: Task.dict) -> TaskResponse:
        return super().edit(uuid, object_)


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
