from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jose import jwt  # noqa
from passlib.context import CryptContext
from starlette import status

from app.schemas.user import UserBase

security = HTTPBearer()

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


def decode_jwt(token: str, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales incorrectas"
        )


def is_authenticated(credentials: HTTPAuthorizationCredentials = Depends(security)):
    secret_key = "YOUR-SECRET-KEY"
    payload = decode_jwt(credentials.credentials, secret_key)

    print(payload)

    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")

    if 'role' not in payload or payload['role'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User does not have access to this endpoint"
        )

    return payload
