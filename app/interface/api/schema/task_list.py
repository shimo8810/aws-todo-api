from typing import Literal, Self

from pydantic import BaseModel

from ....domain.task import Task
from ....domain.task_list import TaskList


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


class TaskListResponse(BaseModel):
    id: str
    name: str
    tasks: list[TaskResponse]

    @classmethod
    def from_domain(cls, task_list: TaskList) -> Self:
        return cls(
            id=str(task_list.id),
            name=str(task_list.name),
            tasks=[
                TaskResponse.from_domain(task)
                for task in task_list.tasks.values()
            ],
        )


class GetTaskListParameters(BaseModel):
    task_list_id: str
    sort_by: Literal["created_at", "title", "status"] = "created_at"
    sort_order: Literal["ascending", "descending"] = "ascending"


class CreateTaskListParameters(BaseModel):
    name: str


class DeleteTaskListParameters(BaseModel):
    task_list_id: str
