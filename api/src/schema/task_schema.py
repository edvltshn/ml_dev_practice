from pydantic import BaseModel
from typing import List

from model.task import Task
from schema.base_schema import FindBase, FindResult


class CreateTaskRequest(BaseModel):
    user_id: str
    text: str
    model_name: str

class CreateTaskResponse(BaseModel):
    task_id: int
    
class HistoryTaskResponse(FindResult):
    ...

class HistoryTaskRequest(FindBase):
    user_id: int=None
