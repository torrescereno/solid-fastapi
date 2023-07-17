from sqlalchemy import Column, Integer, String
from app.dependencies.db import Base


class User(Base):
    __tablename__ = "users"  # noqa

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
