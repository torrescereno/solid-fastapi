import pytest

from pydantic import ValidationError
from app.schemas.user import UserBase, UserCreate, User


def test_user_base_schema():
    user_base = UserBase(username='test_user')

    assert user_base.username == 'test_user'


def test_user_create_schema():
    user_create = UserCreate(username='test_user', password='test_password')

    assert user_create.username == 'test_user'
    assert user_create.password == 'test_password'


def test_user_schema():
    user = User(username='test_user', id=1)

    assert user.username == 'test_user'
    assert user.id == 1


def test_user_base_schema_invalid():
    with pytest.raises(ValidationError):
        UserBase()


def test_user_create_schema_invalid():
    with pytest.raises(ValidationError):
        UserCreate()

    with pytest.raises(ValidationError):
        UserCreate(username='test_user')


def test_user_schema_invalid():
    with pytest.raises(ValidationError):
        User()

    with pytest.raises(ValidationError):
        User(username='test_user')

    with pytest.raises(ValidationError):
        User(username='test_user', id='not_an_integer')
