from google.cloud import firestore

from kanbanize.firestore_adapter import FirestoreAdapter, Model
from kanbanize.tables import database


class TablesAdapter(FirestoreAdapter):
    model = Model
    response_model = Model
    COLLECTION = database.COLLECTION

    def __init__(self, db: firestore.Client = database.get_db()):
        self.db = db

    def get(self, uuid) -> Model:
        return super().get(uuid)

    def create(self, data) -> Model:
        return super().create(new_object=data)

    def edit(self, uuid, data: dict) -> Model:
        return super().edit(uuid, data)
