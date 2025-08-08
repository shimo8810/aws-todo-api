from typing import Self

from pydantic import BaseModel

from ....domain.task_list import TaskList


class TaskListResponse(BaseModel):
    id: str
    user_id: str
    name: str
    count: int

    @classmethod
    def from_domain(cls, task_list: TaskList) -> Self:
        return cls(
            id=str(task_list.id),
            user_id=str(task_list.user_id),
            name=str(task_list.name),
            count=int(task_list.count),
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
