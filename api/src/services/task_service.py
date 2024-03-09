import pika
from fastapi import HTTPException

from repository.task_repository import TaskRepository
from services.base_service import BaseService
from schema.task_schema import CreateTaskRequest, CreateTaskResponse
from core.rabbit import Rabbit


class TaskService(BaseService):

    def __init__(self, task_repository: TaskRepository, queue:Rabbit):
        self.task_repository = task_repository  
        self.queue = queue

    def add(self, schema: CreateTaskRequest) -> CreateTaskResponse:
        try:
            task = self.task_repository.create(schema)
            self.queue.send_task(task)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
  
        return CreateTaskResponse(task_id=task.id)
   
    