from abc import ABC, abstractmethod

from requests import request

from kanbanize.main_api.schemas import Task, TaskResponse


class IAdapter(ABC):
    address: str

    @abstractmethod
    def path(self, endpoint: str):
        path = f"http://{self.address}/{endpoint}"
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
    address = "localhost"

    def create(self, endpoint: str, object_: Task) -> TaskResponse:
        return super().create(endpoint, object_)


class GroupAdapter(IAdapter):
    pass


class TableAdapter(IAdapter):
    pass
