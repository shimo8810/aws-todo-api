from typing import Protocol

from .task_list import TaskList, TaskListId


class TaskListRepository(Protocol):
    def store(self, task_list: TaskList) -> None:
        """Save a task list to the repository."""
        raise NotImplementedError

    def find_by_id(self, task_list_id: TaskListId) -> TaskList | None:
        """Find a task list by its ID."""
        raise NotImplementedError

    def delete(self, task_list_id: TaskListId) -> None:
        """Delete a task list by its ID."""
        raise NotImplementedError

    def list_all(self) -> list[TaskList]:
        """List all task lists in the repository."""
        raise NotImplementedError