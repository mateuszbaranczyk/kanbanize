from kanbanize.firestore_adapter import FirestoreAdapter
from kanbanize.schemas import Task, TaskResponse, TaskUuid
from kanbanize.tasks import database


class TasksAdapter(FirestoreAdapter):
    db = database.get_db()
    model = Task
    response_model = TaskResponse
    COLLECTION = database.COLLECTION

    def get(self, uuid: TaskUuid) -> TaskResponse:
        return super().get(uuid)

    def create(self, data: Task) -> TaskResponse:
        return super().create(new_object=data)

    def edit(self, uuid: TaskUuid, data: dict) -> TaskResponse:
        return super().edit(uuid, data)
