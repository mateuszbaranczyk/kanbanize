from pytest import fixture

from kanbanize.data_structures.schemas import Task


@fixture
def task() -> Task:
    task = Task(name="task_name", status="done", notes="test notes")
    return task


@fixture
def dumped_task(task) -> dict:
    return task.model_dump()
