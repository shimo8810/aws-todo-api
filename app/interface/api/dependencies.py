from typing import Annotated

from fastapi import Depends
from typing_extensions import Self

from ...application.task import TaskService
from ...domain.task_list_repository import TaskListRepository


class InMemoryTaskListRepository(TaskListRepository):
    _instance = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "tasks"):
            self.tasks = []

    def store(self, task_list):
        self.tasks.append(task_list)

    def find_by_id(self, task_list_id):
        for task in self.tasks:
            if task.id == task_list_id:
                return task
        return None

    def delete(self, task_list_id):
        self.tasks = [task for task in self.tasks if task.id != task_list_id]

    def list_all(self):
        return self.tasks


def get_task_list_repository() -> TaskListRepository:
    raise NotImplementedError(
        "Dependency 'get_task_list_repository' has not been overridden."
    )


def get_task_service(
    repo: Annotated[TaskListRepository, Depends(get_task_list_repository)],
) -> TaskService:
    return TaskService(task_list_repository=repo)
