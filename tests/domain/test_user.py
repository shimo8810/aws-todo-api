import uuid

from app.domain.user import User, UserId


def test_user_id_should_store_value():
    # Arrange
    id_value = str(uuid.uuid4())

    # Act
    user_id = UserId(id_value)

    # Assert
    assert user_id.value == id_value
    assert str(user_id) == id_value


def test_user_should_store_id():
    # Arrange
    user_id = UserId(str(uuid.uuid4()))

    # Act
    user = User(user_id)

    # Assert
    assert user.id == user_id
