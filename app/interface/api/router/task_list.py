from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ....application.task import TaskService
from ....domain.task_list import (
    TaskListId,
    TaskListName,
    TaskSortBy,
    TaskSortOrder,
)
from ..dependencies import get_task_service
from ..schema import task_list as schema

router = APIRouter(tags=["task_list"])


@router.get("/task_list/{task_list_id}")
async def get_task_list(
    params: Annotated[
        schema.GetTaskListParameters, Depends(schema.GetTaskListParameters)
    ],
    task_usecase: Annotated[
        TaskService,
        Depends(get_task_service),
    ],
) -> schema.TaskListResponse:
    try:
        task_list_id = TaskListId(value=params.task_list_id)
        sort_by = TaskSortBy(params.sort_by)
        sort_order = TaskSortOrder(params.sort_order)

        task_list = task_usecase.get_task_list(
            task_list_id=task_list_id,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return schema.TaskListResponse.from_domain(task_list)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/task_list")
async def create_task_list(
    params: schema.CreateTaskListParameters,
    task_usecase: Annotated[TaskService, Depends(get_task_service)],
):
    try:
        name = TaskListName(value=params.name)
        task_usecase.create_task_list(name=name)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/task_list/{task_list_id}")
async def delete_task_list(
    params: schema.DeleteTaskListParameters,
    task_usecase: Annotated[TaskService, Depends(get_task_service)],
):
    try:
        task_list_id = TaskListId(params.task_list_id)
        task_usecase.delete_task_list(task_list_id=task_list_id)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/task_list")
async def list_all_task_lists(
    task_usecase: Annotated[TaskService, Depends(get_task_service)],
) -> list[schema.TaskListResponse]:
    try:
        task_lists = task_usecase.list_all_task_lists()
        return [
            schema.TaskListResponse.from_domain(task_list)
            for task_list in task_lists
        ]

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
