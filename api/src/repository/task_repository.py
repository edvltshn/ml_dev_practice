from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from  core.exceptions import NotFoundError
from  model.task import Task
from  repository.base_repository import BaseRepository
from  schema.task_schema import CreateTaskRequest, CreateTaskResponse


class TaskRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Task)

    def create(self, schema: CreateTaskRequest) -> Task:
        with self.session_factory() as session:
            # Создаем новую задачу, используя поля, соответствующие модели Task
            new_task = Task(
                input_data=schema.text,  # Предполагаю, что schema.text соответствует input_data
                predictor=schema.model_name  # и schema.model_name - это имя предиктора
            )
            session.add(new_task)
            session.commit()
            session.refresh(new_task)
            return new_task

    def update_task_with_prediction(self, task_id: int, prediction: str):
        with self.session_factory() as session:
            try:
                task = session.query(self.model).filter(self.model.id == task_id).one()
                task.result = prediction
                task.status = 'completed' 
                session.commit()
            except NoResultFound:
                raise NotFoundError(detail=f"Task with id {task_id} not found.")
