import pika
from fastapi import HTTPException

from repository.task_repository import TaskRepository
from repository.user_repository import UserRepository
from repository.predictor_repository import PredictorRepository
from services.base_service import BaseService
from schema.task_schema import CreateTaskRequest, CreateTaskResponse
from core.rabbit import Rabbit
from model.user import User


class TaskService(BaseService):

    def __init__(self, task_repository: TaskRepository, queue:Rabbit, user_repository:UserRepository, predictor_repository:PredictorRepository):
        self._repository = task_repository  
        self.queue = queue
        self.user_repository = user_repository
        self.predictor_repository = predictor_repository

    def add(self, schema: CreateTaskRequest, user: User) -> CreateTaskResponse:

        try:
            balance = user.blance  
            cost = self.predictor_repository.read_by_name(schema.model_name).cost

            if balance < cost:
                raise HTTPException(status_code=400, detail="Not enough money")
            else:
                new_balance = balance - cost
                        
            task = self._repository.create(schema)
            self.queue.send_task(task)         
            self.user_repository.update_user_balance(user, new_balance)


        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
  
        return CreateTaskResponse(task_id=task.id)
    

   
    