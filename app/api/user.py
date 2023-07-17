from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserBase, User
from app.services.user_service import UserService
from app.dependencies.db import get_db

router = APIRouter()


@router.get("/", response_model=User)
def get_user(username: str, db: Session = Depends(get_db)):
    try:
        user_base = UserBase(username=username)
        service = UserService(db)

        return service.get_user(user_base)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)

    return service.create_user(user)
