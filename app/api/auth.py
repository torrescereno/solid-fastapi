from datetime import timedelta, datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # noqa
from passlib.context import CryptContext
from starlette import status

from app.schemas.user import UserBase

router = APIRouter()

SECRET_KEY = "YOUR-SECRET-KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(user: UserBase, username: str):
    hashed_user = pwd_context.hash(username)

    if username != user.username:
        return False
    if not pwd_context.verify(username, hashed_user):
        return False

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "role": "admin"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token")
def login_for_access_token(username: str):
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
