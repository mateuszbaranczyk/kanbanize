from abc import ABC, abstractmethod
from typing import Any, Dict, Type

import pydantic
from google.cloud import firestore
from schemas import Uuid


class Model(ABC, pydantic.BaseModel):
    uuid: Uuid

    @abstractmethod
    def model_dump(self) -> dict:
        raise NotImplementedError


class DocumentError(Exception):
    pass


class FirestoreAdapter:
    db: firestore.Client
    model: Type[Model]
    response_model: Type[Model]
    DB_TIMEOUT: float = 500.0
    COLLECTION: str

    def create(self, new_object: Model) -> Model:
        db_object = self.response_model(**new_object.model_dump())
        document = self.save_and_get(db_object)
        return self.response_model(**document)

    def get(self, uuid: Uuid) -> Model:
        document = self.get_db_document(uuid)
        if not document.exists:
            raise NameError(f"No such document! {uuid}")
        data = self._document_to_dict(document)
        return self.response_model(**data)

    def edit(self, uuid: Uuid, data: dict) -> Model:
        db_object = self.get(uuid)
        dump = db_object.model_dump()
        updated_object = self._update_obj_data(data, dump)
        edited_document = self.edit_and_get(uuid, updated_object)
        return self.response_model(**edited_document)

    def edit_and_get(self, uuid: Uuid, data: dict) -> Dict[str, Any]:
        document = self.db.collection(self.COLLECTION).document(uuid)
        document.update(data, timeout=self.DB_TIMEOUT)
        edited_document = self.get_db_document(uuid)
        return self._document_to_dict(edited_document)

    def save_and_get(self, db_object: Model) -> Dict[str, Any]:
        dump = db_object.model_dump()
        document = self.db.collection(self.COLLECTION).document(db_object.uuid)
        document.set(dump, timeout=self.DB_TIMEOUT)
        created_document = self.get_db_document(db_object.uuid).to_dict()
        if created_document is None:
            raise DocumentError("Object not created.", dump)
        else:
            return created_document

    def _document_to_dict(
        self, document: firestore.DocumentSnapshot
    ) -> Dict[str, Any]:
        data = document.to_dict()
        if data is None:
            raise DocumentError("Operation faild.")
        else:
            return data

    def _update_obj_data(
        self, data: dict, object_data: dict
    ) -> Dict[str, Any]:
        for key, value in data.items():
            if key in object_data:
                object_data[key] = value
        return object_data

    def get_db_document(self, uuid: Uuid) -> firestore.DocumentSnapshot:
        return self.db.collection(self.COLLECTION).document(uuid).get()
