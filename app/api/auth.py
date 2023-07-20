from datetime import timedelta, datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # noqa
from passlib.context import CryptContext
from starlette import status

from app.schemas.user import UserBase
from app.utils.auth import create_access_token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post("/token")
def access_token(username: str):
    # Obtener usuario de la base de datos
    user = UserBase(username=username)
    user = authenticate_user(user, username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
