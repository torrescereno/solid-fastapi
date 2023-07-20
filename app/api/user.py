from fastapi import APIRouter, Depends, HTTPException
from jose import jwt  # noqa
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserBase, User
from app.services.user_service import UserService
from app.utils.auth import is_authenticated

router = APIRouter()


@router.get("/", response_model=User, dependencies=[Depends(is_authenticated)])
def get_user(username: str, db: Session = Depends(get_db)):
    try:
        user_base = UserBase(username=username)
        service = UserService(db)

        return service.get_user(user_base)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))


@router.post("/", response_model=User, dependencies=[Depends(is_authenticated)])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)

    return service.create_user(user)
