from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm)
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from typing import Dict
from datetime import datetime,timedelta
from config import SECRET_KEY, ALGORITHM, EXPIRE_TIME, Oauth2_scheme
from utils.user import CurrentUser


def create_access_token(data: Dict[str, int]) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_TIME)

    # noinspection PyTypeChecker
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token


def get_current_user(token: str = Depends(Oauth2_scheme)) -> CurrentUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="credentials invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")

        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return CurrentUser(email=email,
                       user_id=user_id)





