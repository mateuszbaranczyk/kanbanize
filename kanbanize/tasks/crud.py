from google.cloud import firestore

from kanbanize.firestore_adapter import FirestoreAdapter
from kanbanize.schemas import Task, TaskResponse, TaskUuid
from kanbanize.tasks import database


class TasksAdapter(FirestoreAdapter):
    model = Task
    response_model = TaskResponse
    COLLECTION = database.COLLECTION

    def __init__(self, db: firestore.Client = database.get_db()):
        self.db = db

    def get(self, uuid: TaskUuid) -> TaskResponse:
        return super().get(uuid)

    def create(self, data: Task) -> TaskResponse:
        return super().create(new_object=data)

    def edit(self, uuid: TaskUuid, data: dict) -> TaskResponse:
        return super().edit(uuid, data)
