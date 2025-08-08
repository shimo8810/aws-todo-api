from datetime import datetime

import pytest

from app.domain.task import (
    Task,
    TaskDescription,
    TaskId,
    TaskStatus,
    TaskTitle,
)
from app.domain.task_list import TaskListId


def test_task_id_generate_should_create_unique_id():
    # Act
    task_id1 = TaskId.generate()
    task_id2 = TaskId.generate()

    # Assert
    assert isinstance(task_id1, TaskId)
    assert isinstance(task_id2, TaskId)
    assert task_id1.value != task_id2.value


def test_task_title_should_create_with_valid_value():
    # Arrange
    valid_title = "Valid Title"

    # Act
    task_title = TaskTitle(valid_title)

    # Assert
    assert task_title.value == valid_title


def test_task_title_should_raise_error_with_empty_value():
    # Act & Assert
    with pytest.raises(ValueError, match="Title cannot be empty."):
        TaskTitle("")


def test_task_title_should_raise_error_with_long_value():
    # Arrange
    long_title = "a" * (TaskTitle.MAX_LENGTH + 1)

    # Act & Assert
    with pytest.raises(
        ValueError,
        match=f"Title exceeds maximum length of {TaskTitle.MAX_LENGTH} "
        "characters.",
    ):
        TaskTitle(long_title)


def test_task_description_should_create_with_valid_value():
    # Arrange
    valid_description = "Valid Description"

    # Act
    task_description = TaskDescription(valid_description)

    # Assert
    assert task_description.value == valid_description


def test_task_description_should_create_with_empty_value():
    # Act
    task_description = TaskDescription("")

    # Assert
    assert task_description.value == ""


def test_task_description_should_raise_error_with_long_value():
    # Arrange
    long_description = "a" * (TaskDescription.MAX_LENGTH + 1)

    # Act & Assert
    with pytest.raises(
        ValueError,
        match="Description exceeds maximum length of "
        f"{TaskDescription.MAX_LENGTH} characters.",
    ):
        TaskDescription(long_description)


def test_task_create_should_initialize_task_correctly():
    # Arrange
    title = TaskTitle("New Task")
    description = TaskDescription("Task Description")
    task_list_id = TaskListId.generate()

    # Act
    task = Task.create(title, description, task_list_id)

    # Assert
    assert isinstance(task, Task)
    assert isinstance(task.id, TaskId)
    assert task.title == title
    assert task.description == description
    assert task.task_list_id == task_list_id
    assert task.status == TaskStatus.TODO
    assert isinstance(task.created_at, datetime)


def test_task_update_title_should_change_title():
    # Arrange
    task = Task.create(
        TaskTitle("Old Title"),
        TaskDescription(""),
        TaskListId.generate(),
    )
    new_title = TaskTitle("New Title")

    # Act
    task.update_title(new_title)

    # Assert
    assert task.title == new_title


def test_task_update_description_should_change_description():
    # Arrange
    task = Task.create(
        TaskTitle("Task"),
        TaskDescription("Old Description"),
        TaskListId.generate(),
    )
    new_description = TaskDescription("New Description")

    # Act
    task.update_description(new_description)

    # Assert
    assert task.description == new_description


def test_task_update_status_should_change_status():
    # Arrange
    task = Task.create(
        TaskTitle("Task"),
        TaskDescription(""),
        TaskListId.generate(),
    )
    assert task.status == TaskStatus.TODO
    new_status = TaskStatus.DONE

    # Act
    task.update_status(new_status)

    # Assert
    assert task.status == new_status
