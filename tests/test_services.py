import pytest
from unittest.mock import MagicMock
from app.models.user import User
from app.schemas.user import UserCreate, UserBase
from app.services.user_service import UserService


def test_create_user_new():
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = None
    user_service = UserService(db_mock)
    new_user = UserCreate(username="newuser", password="password")

    result = user_service.create_user(new_user)

    assert result.username == "newuser"
    assert result.password == "password"

    db_mock.add.assert_called_once_with(result)
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(result)


def test_create_user_existing():
    existing_user = User(username="existinguser", password="password")
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = existing_user
    user_service = UserService(db_mock)
    new_user = UserCreate(username="existinguser", password="password")

    result = user_service.create_user(new_user)

    assert result == existing_user

    db_mock.add.assert_not_called()
    db_mock.commit.assert_not_called()
    db_mock.refresh.assert_not_called()


def test_get_user_existing():
    existing_user = User(username="existinguser", password="password")
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = existing_user
    user_service = UserService(db_mock)
    base_user = UserBase(username="existinguser")

    result = user_service.get_user(base_user)

    assert result == existing_user


def test_get_user_non_existing():
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.side_effect = ValueError("El usuario no existe")
    user_service = UserService(db_mock)
    base_user = UserBase(username="nonexistinguser")

    with pytest.raises(ValueError, match="El usuario no existe"):
        user_service.get_user(base_user)
