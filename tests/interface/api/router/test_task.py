from datetime import datetime
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.domain.task import Task, TaskDescription, TaskId, TaskStatus, TaskTitle
from app.domain.task_list import TaskListId
from app.interface.api.router.task import (
    create_task,
    delete_task,
    get_task,
    list_tasks,
    update_task,
)
from app.interface.api.schema.task import (
    CreateTaskParameters,
    DeleteTaskParameters,
    GetTaskParameters,
    ListTasksParameters,
    UpdateTaskParameters,
)


@pytest.fixture
def mock_todo_service():
    return MagicMock()


@pytest.mark.asyncio
async def test_create_task_should_return_task_response(mock_todo_service):
    # Arrange
    params = CreateTaskParameters(
        task_list_id="list1",
        title="Test Task",
        description="Test Description",
    )
    mock_task = Task(
        id=TaskId("task1"),
        task_list_id=TaskListId("list1"),
        title=TaskTitle("Test Task"),
        description=TaskDescription("Test Description"),
        status=TaskStatus.TODO,
        created_at=datetime.now(),
    )
    mock_todo_service.create_task.return_value = mock_task

    # Act
    response = await create_task(params, mock_todo_service)

    # Assert
    assert response.id == "task1"
    assert response.title == "Test Task"
    mock_todo_service.create_task.assert_called_once()


@pytest.mark.asyncio
async def test_create_task_should_raise_http_exception_on_error(
    mock_todo_service,
):
    # Arrange
    params = CreateTaskParameters(
        task_list_id="list1",
        title="Test Task",
    )
    mock_todo_service.create_task.side_effect = Exception("Test Error")

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await create_task(params, mock_todo_service)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Test Error"


@pytest.mark.asyncio
async def test_list_tasks_should_return_list_of_tasks(mock_todo_service):
    # Arrange
    params = ListTasksParameters(task_list_id="list1")
    mock_tasks = [
        Task(
            id=TaskId("task1"),
            task_list_id=TaskListId("list1"),
            title=TaskTitle("Task 1"),
            description=TaskDescription(""),
            status=TaskStatus.TODO,
            created_at=datetime.now(),
        )
    ]
    mock_todo_service.list_tasks.return_value = mock_tasks

    # Act
    response = await list_tasks(params, mock_todo_service)

    # Assert
    assert len(response) == 1
    assert response[0].id == "task1"
    mock_todo_service.list_tasks.assert_called_once_with(
        task_list_id=TaskListId("list1")
    )


@pytest.mark.asyncio
async def test_get_task_should_return_task(mock_todo_service):
    # Arrange
    params = GetTaskParameters(task_list_id="list1", task_id="task1")
    mock_task = Task(
        id=TaskId("task1"),
        task_list_id=TaskListId("list1"),
        title=TaskTitle("Test Task"),
        description=TaskDescription(""),
        status=TaskStatus.TODO,
        created_at=datetime.now(),
    )
    mock_todo_service.get_task.return_value = mock_task

    # Act
    response = await get_task(params, mock_todo_service)

    # Assert
    assert response.id == "task1"
    mock_todo_service.get_task.assert_called_once_with(task_id=TaskId("task1"))


@pytest.mark.asyncio
async def test_update_task_should_return_updated_task(mock_todo_service):
    # Arrange
    params = UpdateTaskParameters(
        task_list_id="list1",
        task_id="task1",
        title="Updated Title",
        description="Updated Description",
        status="done",
    )
    mock_task = Task(
        id=TaskId("task1"),
        task_list_id=TaskListId("list1"),
        title=TaskTitle("Updated Title"),
        description=TaskDescription("Updated Description"),
        status=TaskStatus.DONE,
        created_at=datetime.now(),
    )
    mock_todo_service.update_task.return_value = mock_task

    # Act
    response = await update_task(params, mock_todo_service)

    # Assert
    assert response.title == "Updated Title"
    assert response.description == "Updated Description"
    assert response.status == TaskStatus.DONE
    mock_todo_service.update_task.assert_called_once()


@pytest.mark.asyncio
async def test_delete_task_should_return_success_message(mock_todo_service):
    # Arrange
    params = DeleteTaskParameters(task_list_id="list1", task_id="task1")

    # Act
    response = await delete_task(params, mock_todo_service)

    # Assert
    assert response == {"message": "Task deleted successfully"}
    mock_todo_service.remove_task.assert_called_once_with(
        task_list_id=TaskListId("list1"), task_id=TaskId("task1")
    )
