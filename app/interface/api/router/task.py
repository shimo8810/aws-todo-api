from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ....application.todo import TodoService
from ....domain.task import Task, TaskDescription, TaskId, TaskStatus, TaskTitle
from ....domain.task_list import (
    TaskListId,
)
from ..dependencies import get_todo_service
from ..schema import task as schema

router = APIRouter(tags=["task"])


@router.post("/task_list/{task_list_id}/task")
async def create_task(
    params: Annotated[
        schema.CreateTaskParameters,
        Depends(schema.CreateTaskParameters),
    ],
    task_usecase: Annotated[
        TodoService,
        Depends(get_todo_service),
    ],
) -> schema.TaskResponse:
    try:
        task_list_id = TaskListId(value=params.task_list_id)
        title = TaskTitle(value=params.title)
        description = TaskDescription(value=params.description or "")

        task = task_usecase.create_task(
            task_list_id=task_list_id,
            title=title,
            description=description,
        )

        return schema.TaskResponse.from_domain(task)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/task_list/{task_list_id}/tasks")
async def list_tasks(
    params: Annotated[
        schema.ListTasksParameters,
        Depends(schema.ListTasksParameters),
    ],
    task_usecase: Annotated[
        TodoService,
        Depends(get_todo_service),
    ],
) -> list[schema.TaskResponse]:
    try:
        task_list_id = TaskListId(value=params.task_list_id)

        tasks = task_usecase.list_tasks(task_list_id=task_list_id)

        return [schema.TaskResponse.from_domain(task) for task in tasks]

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/task_list/{task_list_id}/task/{task_id}")
async def get_task(
    params: Annotated[
        schema.GetTaskParameters,
        Depends(schema.GetTaskParameters),
    ],
    task_usecase: Annotated[
        TodoService,
        Depends(get_todo_service),
    ],
) -> schema.TaskResponse:
    try:
        task_list_id = TaskListId(value=params.task_list_id)
        task_id = TaskId(value=params.task_id)

        task = task_usecase.get_task(
            task_list_id=task_list_id,
            task_id=task_id,
        )

        return schema.TaskResponse.from_domain(task)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.patch("/task_list/{task_list_id}/task/{task_id}")
async def update_task(
    params: Annotated[
        schema.UpdateTaskParameters,
        Depends(schema.UpdateTaskParameters),
    ],
    task_usecase: Annotated[
        TodoService,
        Depends(get_todo_service),
    ],
) -> schema.TaskResponse:
    try:
        task_list_id = TaskListId(value=params.task_list_id)
        task_id = TaskId(value=params.task_id)

        if (
            params.title is None
            and params.description is None
            and params.status is None
        ):
            raise HTTPException(
                status_code=400,
                detail="At least one field (title, description, status) must be provided for update.",
            )

        if params.title is not None:
            title = TaskTitle(value=params.title)
            task = task_usecase.update_task_title(
                task_list_id=task_list_id,
                task_id=task_id,
                title=title,
            )

        if params.description is not None:
            description = TaskDescription(value=params.description)
            task = task_usecase.update_task_description(
                task_list_id=task_list_id,
                task_id=task_id,
                description=description,
            )

        if params.status is not None:
            status = TaskStatus(params.status)
            task = task_usecase.update_task_status(
                task_list_id=task_list_id,
                task_id=task_id,
                status=status,
            )

        return schema.TaskResponse.from_domain(task)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/task_list/{task_list_id}/task/{task_id}")
async def delete_task(
    params: Annotated[
        schema.DeleteTaskParameters,
        Depends(schema.DeleteTaskParameters),
    ],
    task_usecase: Annotated[
        TodoService,
        Depends(get_todo_service),
    ],
):
    try:
        task_list_id = TaskListId(value=params.task_list_id)
        task_id = TaskId(value=params.task_id)

        task_usecase.remove_task(
            task_list_id=task_list_id,
            task_id=task_id,
        )

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
