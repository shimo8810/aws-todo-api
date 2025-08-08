from app.domain.task_list import (
    TaskCount,
    TaskList,
    TaskListId,
    TaskListName,
)
from app.domain.user import UserId
from app.interface.api.schema.task_list import TaskListResponse


def test_task_list_response_from_domain_should_create_correct_response():
    # Arrange
    task_list = TaskList(
        id=TaskListId("list1"),
        user_id=UserId("user1"),
        name=TaskListName("Test List"),
        count=TaskCount(5),
    )

    # Act
    response = TaskListResponse.from_domain(task_list)

    # Assert
    assert response.id == "list1"
    assert response.user_id == "user1"
    assert response.name == "Test List"
    assert response.count == 5
