from abc import ABC, abstractmethod


class IAdapter(ABC):
    address: str
    endpoint: str

    @abstractmethod
    def create(self):
        raise NotImplementedError

    @abstractmethod
    def get(self):
        raise NotImplementedError

    @abstractmethod
    def edit(self):
        raise NotImplementedError


class TaskAdapter(IAdapter):
    pass


class GroupAdapter(IAdapter):
    pass


class TableAdapter(IAdapter):
    pass
