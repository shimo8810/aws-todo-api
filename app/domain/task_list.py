import enum
import uuid
from dataclasses import dataclass
from typing import Self

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


@dataclass(frozen=True)
class TaskCount:
    value: int
    MAX_TASK_COUNT = 100

    def __int__(self) -> int:
        return self.value

    def validate(self) -> None:
        if self.value < 0:
            raise ValueError("Task count cannot be negative.")
        if self.value > self.MAX_TASK_COUNT:
            raise ValueError(f"Task count cannot exceed {self.MAX_TASK_COUNT}.")

    def __post_init__(self) -> None:
        self.validate()


@dataclass
class TaskList:
    id: TaskListId
    user_id: UserId
    name: TaskListName
    count: TaskCount

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
            count=TaskCount(0),
        )

    def update_name(self, name: TaskListName) -> None:
        """Update the name of the task list."""
        self.name = name

    def add_task(self) -> None:
        """Add a task to the task list."""
        self.count = TaskCount(self.count.value + 1)

    def delete_task(self) -> None:
        """Delete a task from the task list."""
        self.count = TaskCount(self.count.value - 1)
