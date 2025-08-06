from typing import Self

from pydantic import BaseModel

from ....domain.task import Task


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str
    created_at: str

    @classmethod
    def from_domain(cls, task: Task) -> Self:
        return cls(
            id=str(task.id),
            title=str(task.title),
            description=str(task.description),
            status=task.status.value,
            created_at=task.created_at.isoformat(),
        )


class GetTaskParameters(BaseModel):
    task_list_id: str
    task_id: str


class CreateTaskParameters(BaseModel):
    task_list_id: str
    title: str
    description: str | None = None


class DeleteTaskParameters(BaseModel):
    task_list_id: str
    task_id: str


class UpdateTaskParameters(BaseModel):
    task_list_id: str
    task_id: str
    title: str | None = None
    description: str | None = None
    status: str | None = None


class ListTasksParameters(BaseModel):
    task_list_id: str
