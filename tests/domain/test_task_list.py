import uuid

import pytest

from app.domain.task_list import (
    TaskCount,
    TaskList,
    TaskListId,
    TaskListName,
)
from app.domain.user import UserId


def test_task_list_id_generate_should_create_unique_id():
    # Act
    task_list_id1 = TaskListId.generate()
    task_list_id2 = TaskListId.generate()

    # Assert
    assert isinstance(task_list_id1, TaskListId)
    assert isinstance(task_list_id2, TaskListId)
    assert task_list_id1.value != task_list_id2.value


def test_task_list_name_should_create_with_valid_value():
    # Arrange
    valid_name = "Valid Name"

    # Act
    task_list_name = TaskListName(valid_name)

    # Assert
    assert task_list_name.value == valid_name


def test_task_list_name_should_raise_error_with_empty_value():
    # Act & Assert
    with pytest.raises(ValueError, match="Task list name cannot be empty."):
        TaskListName("")


def test_task_list_name_should_raise_error_with_long_value():
    # Arrange
    long_name = "a" * (TaskListName.MAX_LENGTH + 1)

    # Act & Assert
    with pytest.raises(
        ValueError,
        match=f"Task list name cannot exceed {TaskListName.MAX_LENGTH} "
        "characters.",
    ):
        TaskListName(long_name)


def test_task_count_should_create_with_valid_value():
    # Arrange
    valid_count = 50

    # Act
    task_count = TaskCount(valid_count)

    # Assert
    assert task_count.value == valid_count


def test_task_count_should_raise_error_with_negative_value():
    # Act & Assert
    with pytest.raises(ValueError, match="Task count cannot be negative."):
        TaskCount(-1)


def test_task_count_should_raise_error_with_large_value():
    # Arrange
    large_count = TaskCount.MAX_TASK_COUNT + 1

    # Act & Assert
    with pytest.raises(
        ValueError,
        match=f"Task count cannot exceed {TaskCount.MAX_TASK_COUNT}.",
    ):
        TaskCount(large_count)


def test_task_list_create_should_initialize_correctly():
    # Arrange
    name = TaskListName("New List")
    user_id = UserId(str(uuid.uuid4()))

    # Act
    task_list = TaskList.create(name, user_id)

    # Assert
    assert isinstance(task_list, TaskList)
    assert isinstance(task_list.id, TaskListId)
    assert task_list.name == name
    assert task_list.user_id == user_id
    assert task_list.count.value == 0


def test_task_list_update_name_should_change_name():
    # Arrange
    task_list = TaskList.create(
        TaskListName("Old Name"),
        UserId(str(uuid.uuid4())),
    )
    new_name = TaskListName("New Name")

    # Act
    task_list.update_name(new_name)

    # Assert
    assert task_list.name == new_name


def test_task_list_add_task_should_increment_count():
    # Arrange
    task_list = TaskList.create(
        TaskListName("List"),
        UserId(str(uuid.uuid4())),
    )
    initial_count = task_list.count.value

    # Act
    task_list.add_task()

    # Assert
    assert task_list.count.value == initial_count + 1


def test_task_list_delete_task_should_decrement_count():
    # Arrange
    task_list = TaskList.create(
        TaskListName("List"),
        UserId(str(uuid.uuid4())),
    )
    task_list.add_task()
    initial_count = task_list.count.value

    # Act
    task_list.delete_task()

    # Assert
    assert task_list.count.value == initial_count - 1
