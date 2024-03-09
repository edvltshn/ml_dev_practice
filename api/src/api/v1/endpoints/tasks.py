from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from  core.container import Container
from  schema.task_schema import CreateTaskRequest, CreateTaskResponse
from  services.task_service import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post("/", response_model=CreateTaskResponse)
@inject
async def create_task(request: CreateTaskRequest, service: TaskService = Depends(Provide[Container.task_service])):
    return service.add(request)