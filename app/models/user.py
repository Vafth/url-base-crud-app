# User models
from sqlmodel import Field, SQLModel
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(index=True, primary_key=True)
    hashed_password: str = Field
    username: str = Field(index=True, unique=True)
    is_admin: bool = False
    is_disabled: bool = False



