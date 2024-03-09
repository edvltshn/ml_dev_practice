from pydantic import BaseModel

class CreateTaskRequest(BaseModel):
    user_id: str
    text: str
    model_name: str


class CreateTaskResponse(BaseModel):
    task_id: int
    
