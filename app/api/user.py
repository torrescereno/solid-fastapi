from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt  # noqa
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserBase, User
from app.services.user_service import UserService

router = APIRouter()
security = HTTPBearer()


def decode_jwt(token: str, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales incorrectas"
        )


def is_authenticated(credentials: HTTPAuthorizationCredentials = Depends(security)):
    secret_key = "YOUR-SECRET-KEY"
    payload = decode_jwt(credentials.credentials, secret_key)

    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication scheme.",
        )

    if "role" not in payload or payload["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to this endpoint",
        )

    return payload


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
