# Task models
from sqlmodel import Field, SQLModel
from typing import Optional

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, index=True, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    task_content: str
    is_complete: bool = False