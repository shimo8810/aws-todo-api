from ..domain.task import Task, TaskDescription, TaskId, TaskStatus, TaskTitle
from ..domain.task_list import (
    TaskList,
    TaskListId,
    TaskListName,
)
from ..domain.task_list_repository import TaskListRepository
from ..domain.task_repository import TaskRepository


class TodoService:
    def __init__(
        self,
        task_list_repository: TaskListRepository,
        task_repository: TaskRepository,
    ):
        self.task_list_repository = task_list_repository
        self.task_repository = task_repository

    def create_task_list(self, name: TaskListName) -> TaskList:
        """Create a new task list."""
        task_list = TaskList.create(name)
        self.task_list_repository.store(task_list)
        return task_list

    def get_task_list(
        self,
        task_list_id: TaskListId,
    ) -> TaskList:
        """Retrieve a task list by its ID."""
        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")

        return task_list

    def update_task_list_name(
        self,
        task_list_id: TaskListId,
        new_name: TaskListName,
    ) -> TaskList:
        """Update the name of an existing task list."""
        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")

        task_list.update_name(new_name)
        self.task_list_repository.store(task_list)

        return task_list

    def delete_task_list(self, task_list_id: TaskListId) -> None:
        """Delete a task list by its ID."""
        self.task_list_repository.delete(task_list_id)

    def list_all_task_lists(self) -> list[TaskList]:
        """List all task lists."""
        return self.task_list_repository.list_all()

    def create_task(
        self,
        task_list_id: TaskListId,
        title: TaskTitle,
        description: TaskDescription,
    ) -> Task:
        """Add a task to an existing task list."""
        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")

        task = Task.create(title, description)
        task_list.add_task(task)

        self.task_list_repository.store(task_list)
        self.task_repository.store(task)

        return task

    def get_task(
        self,
        task_list_id: TaskListId,
        task_id: TaskId,
    ) -> Task:
        """Get a task from a task list by its ID."""
        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")
        if not task_list.includes_task(task_id):
            raise ValueError("Task not found in the task list.")

        task = self.task_repository.find_by_id(task_id)

        if not task:
            raise ValueError("Task not found.")

        return task

    def remove_task(
        self,
        task_list_id: TaskListId,
        task_id: TaskId,
    ) -> None:
        """Remove a task from a task list."""
        task = self.task_repository.find_by_id(task_id)

        if not task:
            raise ValueError("Task not found.")

        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")
        if not task_list.includes_task(task_id):
            raise ValueError("Task not found in the task list.")

        task_list.remove_task(task_id)
        self.task_list_repository.store(task_list)
        self.task_repository.delete(task_id)

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
        if not task_list.includes_task(task_id):
            raise ValueError("Task not found in the task list.")

        task = self.task_repository.find_by_id(task_id)

        if not task:
            raise ValueError("Task not found.")
        task.update_status(status)

        self.task_repository.store(task)

    def update_task_title(
        self,
        task_list_id: TaskListId,
        task_id: TaskId,
        title: TaskTitle,
    ) -> Task:
        """Update the title of a task in a task list."""
        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")
        if not task_list.includes_task(task_id):
            raise ValueError("Task not found in the task list.")

        task = self.task_repository.find_by_id(task_id)

        if not task:
            raise ValueError("Task not found.")

        task.update_title(title)
        self.task_repository.store(task)

        return task

    def update_task_description(
        self,
        task_list_id: TaskListId,
        task_id: TaskId,
        description: TaskDescription,
    ) -> Task:
        """Update the description of a task in a task list."""
        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")
        if not task_list.includes_task(task_id):
            raise ValueError("Task not found in the task list.")

        task = self.task_repository.find_by_id(task_id)

        if not task:
            raise ValueError("Task not found.")

        task.update_description(description)
        self.task_repository.store(task)

        return task

    def list_tasks(
        self,
        task_list_id: TaskListId,
    ) -> list[Task]:
        """List all tasks in a task list with optional sorting."""
        task_list = self.task_list_repository.find_by_id(task_list_id)

        if not task_list:
            raise ValueError("Task list not found.")

        tasks = [
            self.task_repository.find_by_id(task_id)
            for task_id in task_list.tasks
        ]
        tasks = [task for task in tasks if task is not None]

        return tasks
