# User Authentification section
from typing import Annotated
from datetime import datetime, timedelta, timezone

from sqlmodel import select
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param

from starlette.status import HTTP_401_UNAUTHORIZED

import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from pydantic import BaseModel

from app.models.user import User
from app.database import SessionDep
from app.core.config import settings

class Token(BaseModel):
    access_token: str
    token_type:   str

class TokenData(BaseModel):
    username: str | None = None

class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request):
        
        header_authorization: str = request.headers.get("Authorization")

        if header_authorization:
            scheme, params = get_authorization_scheme_param(header_authorization)
            
            if scheme.lower() == "bearer":
                return params

        cookie_authorization: str = request.cookies.get("access_token")

        if not cookie_authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code = HTTP_401_UNAUTHORIZED,
                    detail      = "Not Authenticated",
                    headers     = {"WWW-Authenticate": "Bearer"}
                )

            return None
        
        if cookie_authorization.startswith("Bearer "):
            return cookie_authorization[7:]
        
        return cookie_authorization


pwd_context    = CryptContext(
    schemes    = ["bcrypt"], 
    deprecated = "auto"
)

oauth2_scheme  = OAuth2PasswordBearerWithCookie(
    tokenUrl   = "login",
    auto_error = False
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_hash_password(password):
    return pwd_context.hash(password)

def get_user(session: SessionDep, username: str) -> User | None:
    user = session.exec(select(User).where(User.username == username)).first()
    return user

def authenticate_user(session: SessionDep, username: str, password: str) -> User | None:
    user = get_user(session, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode  = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(
        session: SessionDep, 
        token:   Annotated[str, Depends(oauth2_scheme)] = None
    ):
    
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail      = "Could not validate credentials",
        headers     = {"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception
    try:
        payload  = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
    
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(session=session, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
    ):
    
    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user    

UserDep = Annotated[User, Depends(get_current_active_user)]