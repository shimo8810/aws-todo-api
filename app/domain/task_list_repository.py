from abc import abstractmethod
from typing import Protocol

from .task_list import TaskList, TaskListId
from .user import UserId


class TaskListRepository(Protocol):
    @abstractmethod
    def store(self, task_list: TaskList) -> None:
        """Save a task list to the repository."""
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, task_list_id: TaskListId) -> TaskList | None:
        """Find a task list by its ID."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_list_id: TaskListId) -> None:
        """Delete a task list by its ID."""
        raise NotImplementedError

    @abstractmethod
    def list_all(self, user_id: UserId) -> list[TaskList]:
        """List all task lists in the repository."""
        raise NotImplementedError
