from ..domain.task import Task, TaskDescription, TaskId, TaskStatus, TaskTitle
from ..domain.task_list import (
    TaskList,
    TaskListId,
    TaskListName,
    TaskSortBy,
    TaskSortOrder,
)
from ..domain.task_list_repository import TaskListRepository


class TaskUseCase:
    def __init__(self, task_list_repository: TaskListRepository):
        self.task_list_repository = task_list_repository

    def create_task_list(self, name: TaskListName) -> None:
        """Create a new task list."""
        task_list = TaskList.create(name)
        self.task_list_repository.store(task_list)

    def get_task_list(
        self,
        task_list_id: TaskListId,
        sort_by: TaskSortBy = TaskSortBy.CREATED_AT,
        sort_order: TaskSortOrder = TaskSortOrder.ASCENDING,
    ) -> TaskList:
        """Retrieve a task list by its ID."""
        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")
        task_list.sort_tasks(sort_by, sort_order)
        return task_list

    def update_task_list_name(
        self, task_list_id: TaskListId, new_name: TaskListName
    ) -> None:
        """Update the name of an existing task list."""
        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")

        task_list.name = new_name
        self.task_list_repository.store(task_list)

    def delete_task_list(self, task_list_id: TaskListId) -> None:
        """Delete a task list by its ID."""
        self.task_list_repository.delete(task_list_id)

    def list_all_task_lists(self) -> list[TaskList]:
        """List all task lists."""
        return self.task_list_repository.list_all()

    def add_task_to_list(
        self,
        task_list_id: TaskListId,
        title: TaskTitle,
        description: TaskDescription,
    ) -> None:
        """Add a task to an existing task list."""
        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")

        task = Task.create(title, description)
        task_list.add_task(task)
        self.task_list_repository.store(task_list)

    def get_task_from_list(self, task_list_id: TaskListId, task_id: TaskId) -> Task:
        """Get a task from a task list by its ID."""
        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")
        task = task_list.get_task(task_id)
        if not task:
            raise ValueError("Task not found in the task list.")
        return task

    def remove_task_from_list(self, task_list_id: TaskListId, task_id: TaskId) -> None:
        """Remove a task from a task list."""
        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")

        task_list.remove_task(task_id)
        self.task_list_repository.store(task_list)

    def update_task_status(
        self,
        task_list_id: TaskListId,
        task_id: TaskId,
        status: TaskStatus,
    ) -> None:
        """Update the status of a task in a task list."""
        task_list = self.task_list_repository.find_by_id(task_list_id)
        if not task_list:
            raise ValueError("Task list not found.")

        task = task_list.get_task(task_id)

        if not task:
            raise ValueError("Task not found in the task list.")
        task.status = status
        task_list.update_task(task)
        self.task_list_repository.store(task_list)

    def update_task_title(
        self,
        task_list_id: TaskListId,
        task_id: TaskId,
        title: TaskTitle,
    ) -> None:
        """Update the title of a task in a task list."""
        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")

        task = task_list.get_task(task_id)
        if not task:
            raise ValueError("Task not found in the task list.")

        task.title = title
        task_list.update_task(task)
        self.task_list_repository.store(task_list)

    def update_task_description(
        self,
        task_list_id: TaskListId,
        task_id: TaskId,
        description: TaskDescription,
    ) -> None:
        """Update the description of a task in a task list."""
        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")

        task = task_list.get_task(task_id)
        if not task:
            raise ValueError("Task not found in the task list.")

        task.description = description
        task_list.update_task(task)
        self.task_list_repository.store(task_list)
