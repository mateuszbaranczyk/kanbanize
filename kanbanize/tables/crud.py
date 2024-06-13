from google.cloud import firestore

from kanbanize.firestore_adapter import FirestoreAdapter
from kanbanize.schemas import Table, TableResponse, TableUuid
from kanbanize.tables import database


class TablesAdapter(FirestoreAdapter):
    model = Table
    response_model = TableResponse
    COLLECTION = database.COLLECTION

    def __init__(self, db: firestore.Client = database.get_db()):
        self.db = db

    def get(self, uuid: TableUuid) -> TableResponse:
        return super().get(uuid)

    def create(self, data: Table) -> TableResponse:
        return super().create(new_object=data)

    def edit(self, uuid: TableUuid, data: dict) -> TableResponse:
        return super().edit(uuid, data)
