import uuid
from datetime import datetime
from unittest.mock import MagicMock

import pytest

from app.application.todo import TodoService
from app.domain.task import Task, TaskDescription, TaskId, TaskStatus, TaskTitle
from app.domain.task_list import TaskCount, TaskList, TaskListId, TaskListName
from app.domain.task_list_repository import TaskListRepository
from app.domain.task_repository import TaskRepository
from app.domain.user import UserId


@pytest.fixture
def mock_task_list_repository():
    return MagicMock(spec=TaskListRepository)


@pytest.fixture
def mock_task_repository():
    return MagicMock(spec=TaskRepository)


@pytest.fixture
def todo_service(mock_task_list_repository, mock_task_repository):
    return TodoService(mock_task_list_repository, mock_task_repository)


def test_create_task_list_should_create_and_store_task_list(
    todo_service: TodoService,
    mock_task_list_repository: MagicMock,
):
    # Arrange
    user_id = UserId(str(uuid.uuid4()))
    name = TaskListName("Test Task List")

    # Act
    task_list = todo_service.create_task_list(user_id, name)

    # Assert
    assert isinstance(task_list, TaskList)
    assert task_list.name == name
    assert task_list.user_id == user_id
    mock_task_list_repository.store.assert_called_once_with(task_list)


def test_get_task_list_should_return_task_list_when_found(
    todo_service: TodoService,
    mock_task_list_repository: MagicMock,
):
    # Arrange
    task_list_id = TaskListId(str(uuid.uuid4()))
    expected_task_list = TaskList(
        id=task_list_id,
        name=TaskListName("Test"),
        user_id=UserId(str(uuid.uuid4())),
        count=TaskCount(0),
    )
    mock_task_list_repository.find_by_id.return_value = expected_task_list

    # Act
    task_list = todo_service.get_task_list(task_list_id)

    # Assert
    assert task_list == expected_task_list
    mock_task_list_repository.find_by_id.assert_called_once_with(task_list_id)


def test_get_task_list_should_raise_error_when_not_found(
    todo_service: TodoService,
    mock_task_list_repository: MagicMock,
):
    # Arrange
    task_list_id = TaskListId(str(uuid.uuid4()))
    mock_task_list_repository.find_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match="Task list not found."):
        todo_service.get_task_list(task_list_id)
    mock_task_list_repository.find_by_id.assert_called_once_with(task_list_id)


def test_update_task_list_name_should_update_and_store_task_list(
    todo_service: TodoService,
    mock_task_list_repository: MagicMock,
):
    # Arrange
    task_list_id = TaskListId(str(uuid.uuid4()))
    old_name = TaskListName("Old Name")
    new_name = TaskListName("New Name")
    task_list = TaskList(
        id=task_list_id,
        name=old_name,
        user_id=UserId(str(uuid.uuid4())),
        count=TaskCount(0),
    )
    mock_task_list_repository.find_by_id.return_value = task_list

    # Act
    updated_task_list = todo_service.update_task_list_name(
        task_list_id,
        new_name,
    )

    # Assert
    assert updated_task_list.name == new_name
    mock_task_list_repository.find_by_id.assert_called_once_with(task_list_id)
    mock_task_list_repository.store.assert_called_once_with(updated_task_list)


def test_update_task_list_name_should_raise_error_when_not_found(
    todo_service: TodoService,
    mock_task_list_repository: MagicMock,
):
    # Arrange
    task_list_id = TaskListId(str(uuid.uuid4()))
    new_name = TaskListName("New Name")
    mock_task_list_repository.find_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match="Task list not found."):
        todo_service.update_task_list_name(task_list_id, new_name)
    mock_task_list_repository.find_by_id.assert_called_once_with(task_list_id)


def test_delete_task_list_should_call_delete_on_repository(
    todo_service: TodoService,
    mock_task_list_repository: MagicMock,
):
    # Arrange
    task_list_id = TaskListId(str(uuid.uuid4()))

    # Act
    todo_service.delete_task_list(task_list_id)

    # Assert
    mock_task_list_repository.delete.assert_called_once_with(task_list_id)


def test_list_all_task_lists_should_return_list_from_repository(
    todo_service: TodoService,
    mock_task_list_repository: MagicMock,
):
    # Arrange
    user_id = UserId(str(uuid.uuid4()))
    expected_lists = [
        TaskList(
            id=TaskListId(str(uuid.uuid4())),
            name=TaskListName("List 1"),
            user_id=user_id,
            count=TaskCount(0),
        )
    ]
    mock_task_list_repository.list_all.return_value = expected_lists

    # Act
    task_lists = todo_service.list_all_task_lists(user_id)

    # Assert
    assert task_lists == expected_lists
    mock_task_list_repository.list_all.assert_called_once_with(user_id)


def test_create_task_should_create_and_store_task(
    todo_service: TodoService,
    mock_task_list_repository: MagicMock,
    mock_task_repository: MagicMock,
):
    # Arrange
    task_list_id = TaskListId(str(uuid.uuid4()))
    title = TaskTitle("Test Task")
    description = TaskDescription("Test Description")
    task_list = TaskList(
        id=task_list_id,
        name=TaskListName("Test List"),
        user_id=UserId(str(uuid.uuid4())),
        count=TaskCount(0),
    )
    mock_task_list_repository.find_by_id.return_value = task_list

    # Act
    task = todo_service.create_task(task_list_id, title, description)

    # Assert
    assert isinstance(task, Task)
    assert task.title == title
    assert task.description == description
    assert task.task_list_id == task_list_id
    assert task_list.count.value == 1
    mock_task_list_repository.find_by_id.assert_called_once_with(task_list_id)
    mock_task_list_repository.store.assert_called_once_with(task_list)
    mock_task_repository.store.assert_called_once_with(task)


def test_create_task_should_raise_error_when_task_list_not_found(
    todo_service: TodoService,
    mock_task_list_repository: MagicMock,
):
    # Arrange
    task_list_id = TaskListId(str(uuid.uuid4()))
    title = TaskTitle("Test Task")
    description = TaskDescription("Test Description")
    mock_task_list_repository.find_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match="Task list not found."):
        todo_service.create_task(task_list_id, title, description)
    mock_task_list_repository.find_by_id.assert_called_once_with(task_list_id)


def test_get_task_should_return_task_when_found(
    todo_service: TodoService,
    mock_task_repository: MagicMock,
):
    # Arrange
    task_id = TaskId(str(uuid.uuid4()))
    expected_task = Task(
        id=task_id,
        title=TaskTitle("Test"),
        description=TaskDescription("Test"),
        status=TaskStatus.TODO,
        task_list_id=TaskListId(str(uuid.uuid4())),
        created_at=datetime.now(),
    )
    mock_task_repository.find_by_id.return_value = expected_task

    # Act
    task = todo_service.get_task(task_id)

    # Assert
    assert task == expected_task
    mock_task_repository.find_by_id.assert_called_once_with(task_id)


def test_get_task_should_raise_error_when_not_found(
    todo_service: TodoService,
    mock_task_repository: MagicMock,
):
    # Arrange
    task_id = TaskId(str(uuid.uuid4()))
    mock_task_repository.find_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match="Task not found."):
        todo_service.get_task(task_id)
    mock_task_repository.find_by_id.assert_called_once_with(task_id)
