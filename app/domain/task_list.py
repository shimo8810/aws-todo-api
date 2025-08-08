import enum
import uuid
from dataclasses import dataclass
from typing import Self

from .task import Task, TaskId
from .user import UserId


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
    user_id: UserId
    name: TaskListName
    tasks: list[TaskId]
    MAX_TASKS = 1000

    @classmethod
    def create(
        cls,
        name: TaskListName,
        user_id: UserId,
    ) -> Self:
        return cls(
            id=TaskListId.generate(),
            user_id=user_id,
            name=name,
            tasks=[],
        )

    def add_task(self, task: Task) -> None:
        """Add a task to the task list."""
        if len(self.tasks) >= self.MAX_TASKS:
            raise ValueError(
                f"Cannot add more than {self.MAX_TASKS} tasks to a task list."
            )
        self.tasks.append(task.id)

    def remove_task(self, task_id: TaskId) -> None:
        """Remove a task from the task list by its ID."""
        self.tasks.remove(task_id)

    def includes_task(self, task_id: TaskId) -> bool:
        """Check if the task list includes a task by its ID."""
        return task_id in self.tasks

    def update_name(self, name: TaskListName) -> None:
        """Update the name of the task list."""
        self.name = name
