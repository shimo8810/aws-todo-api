import enum
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Self


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
                f"Description exceeds maximum length of {self.MAX_LENGTH} characters."
            )

    def __post_init__(self) -> None:
        self.validate()


class TaskStatus(enum.StrEnum):
    TODO = enum.auto()
    DONE = enum.auto()
    DELETED = enum.auto()


@dataclass
class Task:
    id: TaskId
    title: TaskTitle
    description: TaskDescription
    status: TaskStatus
    created_at: datetime

    @classmethod
    def create(
        cls,
        title: str,
        description: str,
    ) -> Self:
        return cls(
            id=TaskId.generate(),
            title=TaskTitle(title),
            description=TaskDescription(description),
            status=TaskStatus.TODO,
            created_at=datetime.now(),
        )
