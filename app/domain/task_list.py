import enum
import uuid
from dataclasses import dataclass
from typing import Self

from .task import Task, TaskId


@dataclass(frozen=True)
class TaskListId:
    value: str

    def __str__(self) -> str:
        return self.value

    @classmethod
    def generate(cls) -> Self:
        return cls(value=str(uuid.uuid4()))


@dataclass(frozen=True)
class TaskListName:
    value: str
    MAX_LENGTH = 100

    def __str__(self) -> str:
        return self.value

    def validate(self) -> None:
        if not self.value:
            raise ValueError("Task list name cannot be empty.")
        if len(self.value) > self.MAX_LENGTH:
            raise ValueError(
                f"Task list name cannot exceed {self.MAX_LENGTH} characters."
            )

    def __post_init__(self) -> None:
        self.validate()


class TaskSortOrder(enum.StrEnum):
    ASCENDING = enum.auto()
    DESCENDING = enum.auto()

    @classmethod
    def default(cls) -> "TaskSortOrder":
        return cls.ASCENDING


class TaskSortBy(enum.StrEnum):
    CREATED_AT = enum.auto()
    TITLE = enum.auto()
    STATUS = enum.auto()

    @classmethod
    def default(cls) -> "TaskSortBy":
        return cls.CREATED_AT


@dataclass
class TaskList:
    id: TaskListId
    name: TaskListName
    tasks: dict[TaskId, Task]

    @classmethod
    def create(
        cls,
        name: TaskListName,
    ) -> Self:
        return cls(
            id=TaskListId.generate(),
            name=name,
            tasks={},
        )

    def add_task(self, task: Task) -> None:
        """Add a task to the task list."""
        self.tasks[task.id] = task

    def sort_tasks(
        self,
        sort_by: TaskSortBy,
        sort_order: TaskSortOrder,
    ) -> None:
        """Sort tasks in the task list."""
        sorted_tasks = sorted(
            self.tasks.values(),
            key=lambda x: getattr(x, sort_by.value),
            reverse=sort_order == TaskSortOrder.DESCENDING,
        )
        self.tasks = {task.id: task for task in sorted_tasks}

    def remove_task(self, task_id: TaskId) -> None:
        """Remove a task from the task list by its ID."""
        self.tasks.pop(task_id, None)

    def update_task(self, updated_task: Task) -> None:
        """Update a task in the task list."""
        self.tasks[updated_task.id] = updated_task

    def get_task(self, task_id: TaskId) -> Task | None:
        """Get a task by its ID."""
        return self.tasks.get(task_id)
