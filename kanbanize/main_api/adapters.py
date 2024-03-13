from abc import ABC, abstractmethod

from requests import request

from kanbanize.main_api.schemas import (
    Group,
    GroupResponse,
    Table,
    TableResponse,
    Task,
    TaskResponse,
)


class IAdapter(ABC):
    location: str

    @abstractmethod
    def path(self, endpoint: str):
        path = f"http://{self.location}/{endpoint}"
        return path

    @abstractmethod
    def create(self, endpoint, object_):
        path = self.path(endpoint)
        result = request.post(path, object_)
        return result

    @abstractmethod
    def get(self, endpoint, uuid):
        path = self.path(endpoint)
        url = f"{path}/{uuid}/"
        result = request.get(url)
        return result

    @abstractmethod
    def edit(self, endpoint, uuid, object_):
        path = self.path(endpoint)
        url = f"{path}/{endpoint}/{uuid}"
        result = request.patch(url, object_)
        return result


class TaskAdapter(IAdapter):
    location = "localhost"

    def create(self, endpoint: str, object_: Task) -> TaskResponse:
        return super().create(endpoint, object_)

    def get(self, endpoint: str, uuid: str) -> TaskResponse:
        return super().get(endpoint, uuid)

    def edit(self, endpoint: str, uuid: str, object_: Task) -> TaskResponse:
        return super().edit(endpoint, uuid, object_)


class GroupAdapter(IAdapter):
    location = "localhost"

    def create(self, endpoint: str, object_: Group) -> GroupResponse:
        return super().create(endpoint, object_)

    def get(self, endpoint: str, uuid: str) -> GroupResponse:
        return super().get(endpoint, uuid)

    def edit(self, endpoint: str, uuid: str, object_: Group) -> GroupResponse:
        return super().edit(endpoint, uuid, object_)


class TableAdapter(IAdapter):
    location = "localhost"

    def create(self, endpoint: str, object_: Table) -> TableResponse:
        return super().create(endpoint, object_)

    def get(self, endpoint: str, uuid: str) -> TableResponse:
        return super().get(endpoint, uuid)

    def edit(self, endpoint: str, uuid: str, object_: Table) -> TableResponse:
        return super().edit(endpoint, uuid, object_)
