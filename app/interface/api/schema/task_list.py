from typing import Self

from pydantic import BaseModel

from ....domain.task_list import TaskList


class TaskListResponse(BaseModel):
    id: str
    name: str
    tasks: list[str]

    @classmethod
    def from_domain(cls, task_list: TaskList) -> Self:
        return cls(
            id=str(task_list.id),
            name=str(task_list.name),
            tasks=[str(task_id) for task_id in task_list.tasks],
        )


class GetTaskListParameters(BaseModel):
    task_list_id: str


class CreateTaskListParameters(BaseModel):
    name: str


class DeleteTaskListParameters(BaseModel):
    task_list_id: str


class UpdateTaskListParameters(BaseModel):
    task_list_id: str
    name: str
