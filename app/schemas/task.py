from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    user_id: int 
    task_content: str
    is_complete: bool = False

class TaskUpdate(BaseModel):
    id: int
    task_content: Optional[str] = None
    is_complete: Optional[bool] = None