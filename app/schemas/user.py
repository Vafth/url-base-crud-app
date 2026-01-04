from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    password: str
    username: str
    is_admin: bool = False
    is_disabled: bool = False

class UserPublic(BaseModel):
    id: int
    username: str
    is_admin: bool = False
    is_disabled: bool = False

class UserTest(BaseModel):
    user_id: int 
    username: str 
    password: str
    is_admin: bool
    token: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    is_disabled: Optional[bool] = None