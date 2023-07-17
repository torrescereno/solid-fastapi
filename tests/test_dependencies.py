from app.dependencies.db import get_db
from sqlalchemy.orm import Session


def test_get_db():
    assert isinstance(next(get_db("test")), Session)
