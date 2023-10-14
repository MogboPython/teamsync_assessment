from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)
from jose import jwt, JWTError
from schemas import UserData
from models import User, SessionLocal

session = SessionLocal()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )

        username: str = payload.get("sub")
        expire: datetime = payload.get("exp")

        if username is None:
            raise credentials_exception
        # token_data = UserData(username=username)

        if datetime.fromtimestamp(expire) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(JWTError):
        raise credentials_exception
    
    user = session.query(User).filter_by(username=username).first() 
    if user is None:
        raise credentials_exception
    
    return username

# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user