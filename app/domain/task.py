import enum
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Self

from .task_list import TaskListId


@dataclass(frozen=True)
class TaskId:
    value: str

    def __str__(self) -> str:
        return self.value

    @classmethod
    def generate(cls) -> Self:
        return cls(value=str(uuid.uuid4()))


@dataclass(frozen=True)
class TaskTitle:
    value: str

    MAX_LENGTH = 100

    def __str__(self) -> str:
        return self.value

    def validate(self) -> None:
        if not self.value:
            raise ValueError("Title cannot be empty.")
        if len(self.value) > self.MAX_LENGTH:
            raise ValueError(
                f"Title exceeds maximum length of {self.MAX_LENGTH} characters."
            )

    def __post_init__(self) -> None:
        self.validate()


@dataclass(frozen=True)
class TaskDescription:
    value: str

    MAX_LENGTH = 500

    def __str__(self) -> str:
        return self.value

    def validate(self) -> None:
        if len(self.value) > self.MAX_LENGTH:
            raise ValueError(
                f"Description exceeds maximum length of {self.MAX_LENGTH} characters."  # noqa
            )

    def __post_init__(self) -> None:
        self.validate()


class TaskStatus(enum.StrEnum):
    TODO = enum.auto()
    DONE = enum.auto()


@dataclass
class Task:
    id: TaskId
    task_list_id: TaskListId
    title: TaskTitle
    description: TaskDescription
    status: TaskStatus
    created_at: datetime

    @classmethod
    def create(
        cls,
        title: TaskTitle,
        description: TaskDescription,
        task_list_id: TaskListId,
    ) -> Self:
        return cls(
            id=TaskId.generate(),
            task_list_id=task_list_id,
            title=title,
            description=description,
            status=TaskStatus.TODO,
            created_at=datetime.now(),
        )

    def update_title(self, title: TaskTitle) -> None:
        """Update the title of the task."""
        self.title = title

    def update_description(self, description: TaskDescription) -> None:
        """Update the description of the task."""
        self.description = description

    def update_status(self, status: TaskStatus) -> None:
        """Update the status of the task."""
        self.status = status
