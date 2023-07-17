import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from fastapi.testclient import TestClient
from app.dependencies.db import get_db, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_test() -> Session:
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client() -> TestClient:
    app.dependency_overrides[get_db] = get_db_test  # noqa
    with TestClient(app) as c:
        yield c
