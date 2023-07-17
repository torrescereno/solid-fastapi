from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserBase


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate):
        db_user = self.db.query(User).filter(User.username == user.username).first()

        if db_user:
            return db_user

        db_user = User(username=user.username, password=user.password)

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def get_user(self, user: UserBase):
        db_user = self.db.query(User).filter(User.username == user.username).first()

        if not db_user:
            raise ValueError("El usuario no existe")

        return db_user
