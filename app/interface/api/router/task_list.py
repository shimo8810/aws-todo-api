from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from ....application.todo import TodoService
from ....domain.task_list import (
    TaskListId,
    TaskListName,
)
from ....domain.user import UserId
from ..dependencies import get_todo_service
from ..schema import task_list as schema

router = APIRouter(tags=["task_list"])


@router.post("/task_list")
async def create_task_list(
    params: Annotated[
        schema.CreateTaskListParameters,
        Depends(schema.CreateTaskListParameters),
    ],
    task_usecase: Annotated[
        TodoService,
        Depends(get_todo_service),
    ],
) -> schema.TaskListResponse:
    try:
        name = TaskListName(value=params.name)
        user_id = UserId("000001")
        task_list = task_usecase.create_task_list(user_id, name)
        return schema.TaskListResponse.from_domain(task_list)
    except Exception as e:
        logger.exception(f"Error creating task list: {e}")
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/task_list")
async def list_all_task_lists(
    task_usecase: Annotated[
        TodoService,
        Depends(get_todo_service),
    ],
) -> list[schema.TaskListResponse]:
    try:
        task_lists = task_usecase.list_all_task_lists(user_id=UserId("000001"))
        return [
            schema.TaskListResponse.from_domain(task_list)
            for task_list in task_lists
        ]

    except Exception as e:
        logger.exception(f"Error listing task lists: {e}")
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/task_list/{task_list_id}")
async def get_task_list(
    params: Annotated[
        schema.GetTaskListParameters,
        Depends(schema.GetTaskListParameters),
    ],
    task_usecase: Annotated[
        TodoService,
        Depends(get_todo_service),
    ],
) -> schema.TaskListResponse:
    try:
        task_list_id = TaskListId(value=params.task_list_id)

        task_list = task_usecase.get_task_list(
            task_list_id=task_list_id,
        )
        return schema.TaskListResponse.from_domain(task_list)

    except Exception as e:
        logger.exception(f"Error getting task list: {e}")
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.patch("/task_list/{task_list_id}")
async def update_task_list(
    params: Annotated[
        schema.UpdateTaskListParameters,
        Depends(schema.UpdateTaskListParameters),
    ],
    task_usecase: Annotated[
        TodoService,
        Depends(get_todo_service),
    ],
) -> schema.TaskListResponse:
    try:
        name = TaskListName(value=params.name)
        task_list_id = TaskListId(params.task_list_id)

        task_list = task_usecase.update_task_list_name(
            task_list_id=task_list_id,
            new_name=name,
        )

        return schema.TaskListResponse.from_domain(task_list)

    except Exception as e:
        logger.exception(f"Error updating task list: {e}")
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/task_list/{task_list_id}")
async def delete_task_list(
    params: Annotated[
        schema.DeleteTaskListParameters,
        Depends(schema.DeleteTaskListParameters),
    ],
    task_usecase: Annotated[
        TodoService,
        Depends(get_todo_service),
    ],
):
    try:
        task_list_id = TaskListId(params.task_list_id)
        task_usecase.delete_task_list(task_list_id=task_list_id)

    except Exception as e:
        logger.exception(f"Error deleting task list: {e}")
        raise HTTPException(status_code=404, detail=str(e)) from e
