import os
import uuid

from google.cloud import firestore

from kanbanize.data_structures.schemas import TaskResponse

project_id = os.getenv("PROJECT_ID")
db = firestore.Client(project=project_id, database="kanbanize")


uuid = str(uuid.uuid4())
task_id = f"ta-{uuid}"
task = TaskResponse(name="front", status="TODO", notes="test", uuid=task_id)
task_dump = task.model_dump()

doc_ref = db.collection("tasks").document(task_id)
doc_ref.set(task_dump, timeout=500.0)


# https://cloud.google.com/firestore/docs/manage-data/add-data
