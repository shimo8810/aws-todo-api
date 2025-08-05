from unittest.mock import MagicMock

import pytest

from app.domain.task_list import TaskList
from app.domain.task_list_repository import TaskListRepository


@pytest.fixture
def mock_task_list_repository() -> TaskListRepository:
    """Provides a mock of the TaskListRepository."""
    return MagicMock(spec=TaskListRepository)


@pytest.fixture
def task_list_factory():
    """Provides a factory for creating TaskList instances."""

    def _factory(name="Test List"):
        return TaskList.create(name=name)

    return _factory


def test_store_task_list(
    mock_task_list_repository: TaskListRepository, task_list_factory
):
    """Test that the store method is called correctly."""
    # Arrange
    task_list = task_list_factory()

    # Act
    mock_task_list_repository.store(task_list)

    # Assert
    mock_task_list_repository.store.assert_called_once_with(task_list)


def test_find_by_id_returns_task_list(
    mock_task_list_repository: TaskListRepository, task_list_factory
):
    """Test that find_by_id returns a task list when it exists."""
    # Arrange
    task_list = task_list_factory()
    mock_task_list_repository.find_by_id.return_value = task_list

    # Act
    found_task_list = mock_task_list_repository.find_by_id(task_list.id)

    # Assert
    mock_task_list_repository.find_by_id.assert_called_once_with(task_list.id)
    assert found_task_list == task_list


def test_find_by_id_returns_none_when_not_found(
    mock_task_list_repository: TaskListRepository, task_list_factory
):
    """Test that find_by_id returns None when the task list does not exist."""
    # Arrange
    task_list = task_list_factory()
    mock_task_list_repository.find_by_id.return_value = None

    # Act
    found_task_list = mock_task_list_repository.find_by_id(task_list.id)

    # Assert
    mock_task_list_repository.find_by_id.assert_called_once_with(task_list.id)
    assert found_task_list is None
