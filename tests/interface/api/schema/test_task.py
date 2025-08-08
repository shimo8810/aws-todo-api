from datetime import datetime

from app.domain.task import Task, TaskDescription, TaskId, TaskStatus, TaskTitle
from app.domain.task_list import TaskListId
from app.interface.api.schema.task import TaskResponse


def test_task_response_from_domain_should_create_correct_response():
    # Arrange
    now = datetime.now()
    task = Task(
        id=TaskId("task1"),
        task_list_id=TaskListId("list1"),
        title=TaskTitle("Test Task"),
        description=TaskDescription("Test Description"),
        status=TaskStatus.TODO,
        created_at=now,
    )

    # Act
    response = TaskResponse.from_domain(task)

    # Assert
    assert response.id == "task1"
    assert response.title == "Test Task"
    assert response.description == "Test Description"
    assert response.status == "todo"
    assert response.created_at == now.isoformat()
