from abc import abstractmethod
from typing import Protocol

from .task import Task, TaskId
from .task_list import TaskListId


class TaskRepository(Protocol):
    @abstractmethod
    def store(
        self,
        task: Task,
    ) -> None:
        """Save a task to the repository."""
        raise NotImplementedError

    @abstractmethod
    def find_by_id(
        self,
        task_id: TaskId,
    ) -> Task | None:
        """Find a task by its ID."""
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        task_id: TaskId,
    ) -> None:
        """Delete a task by its ID."""
        raise NotImplementedError

    @abstractmethod
    def list_all(self, task_list_id: TaskListId) -> list[Task]:
        """List all tasks in the repository."""
        raise NotImplementedError
