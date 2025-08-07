from typing import Annotated

from fastapi import Depends

from ...application.todo import TodoService
from ...domain.task_list_repository import TaskListRepository
from ...domain.task_repository import TaskRepository


def get_task_list_repository() -> TaskListRepository:
    raise NotImplementedError(
        "Dependency 'get_task_list_repository' has not been overridden."
    )


def get_task_repository() -> TaskRepository:
    raise NotImplementedError(
        "Dependency 'get_task_repository' has not been overridden."
    )


def get_todo_service(
    task_list_repository: Annotated[
        TaskListRepository,
        Depends(get_task_list_repository),
    ],
    task_repository: Annotated[
        TaskRepository,
        Depends(get_task_repository),
    ],
) -> TodoService:
    return TodoService(
        task_list_repository=task_list_repository,
        task_repository=task_repository,
    )
