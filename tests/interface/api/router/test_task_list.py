from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.domain.task_list import TaskCount, TaskList, TaskListId, TaskListName
from app.domain.user import UserId
from app.interface.api.router.task_list import (
    create_task_list,
    delete_task_list,
    get_task_list,
    list_all_task_lists,
    update_task_list,
)
from app.interface.api.schema.task_list import (
    CreateTaskListParameters,
    DeleteTaskListParameters,
    GetTaskListParameters,
    UpdateTaskListParameters,
)


@pytest.fixture
def mock_todo_service():
    return MagicMock()


@pytest.mark.asyncio
async def test_create_task_list_should_return_task_list_response(
    mock_todo_service,
):
    # Arrange
    params = CreateTaskListParameters(name="Test List")
    mock_list = TaskList(
        id=TaskListId("list1"),
        name=TaskListName("Test List"),
        user_id=UserId("user1"),
        count=TaskCount(0),
    )
    mock_todo_service.create_task_list.return_value = mock_list

    # Act
    response = await create_task_list(params, mock_todo_service)

    # Assert
    assert response.id == "list1"
    assert response.name == "Test List"
    mock_todo_service.create_task_list.assert_called_once()


@pytest.mark.asyncio
async def test_create_task_list_should_raise_http_exception_on_error(
    mock_todo_service,
):
    # Arrange
    params = CreateTaskListParameters(name="Test List")
    mock_todo_service.create_task_list.side_effect = Exception("Test Error")

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await create_task_list(params, mock_todo_service)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Test Error"


@pytest.mark.asyncio
async def test_list_all_task_lists_should_return_list_of_task_lists(
    mock_todo_service,
):
    # Arrange
    mock_lists = [
        TaskList(
            id=TaskListId("list1"),
            name=TaskListName("List 1"),
            user_id=UserId("user1"),
            count=TaskCount(0),
        )
    ]
    mock_todo_service.list_all_task_lists.return_value = mock_lists

    # Act
    response = await list_all_task_lists(mock_todo_service)

    # Assert
    assert len(response) == 1
    assert response[0].id == "list1"
    mock_todo_service.list_all_task_lists.assert_called_once()


@pytest.mark.asyncio
async def test_get_task_list_should_return_task_list(mock_todo_service):
    # Arrange
    params = GetTaskListParameters(task_list_id="list1")
    mock_list = TaskList(
        id=TaskListId("list1"),
        name=TaskListName("Test List"),
        user_id=UserId("user1"),
        count=TaskCount(0),
    )
    mock_todo_service.get_task_list.return_value = mock_list

    # Act
    response = await get_task_list(params, mock_todo_service)

    # Assert
    assert response.id == "list1"
    mock_todo_service.get_task_list.assert_called_once_with(
        task_list_id=TaskListId("list1")
    )


@pytest.mark.asyncio
async def test_update_task_list_should_return_updated_task_list(
    mock_todo_service,
):
    # Arrange
    params = UpdateTaskListParameters(task_list_id="list1", name="Updated Name")
    mock_list = TaskList(
        id=TaskListId("list1"),
        name=TaskListName("Updated Name"),
        user_id=UserId("user1"),
        count=TaskCount(0),
    )
    mock_todo_service.update_task_list_name.return_value = mock_list

    # Act
    response = await update_task_list(params, mock_todo_service)

    # Assert
    assert response.name == "Updated Name"
    mock_todo_service.update_task_list_name.assert_called_once()


@pytest.mark.asyncio
async def test_delete_task_list_should_return_success_message(
    mock_todo_service,
):
    # Arrange
    params = DeleteTaskListParameters(task_list_id="list1")

    # Act
    response = await delete_task_list(params, mock_todo_service)

    # Assert
    assert response == {"message": "Task list deleted successfully"}
    mock_todo_service.delete_task_list.assert_called_once_with(
        task_list_id=TaskListId("list1")
    )
