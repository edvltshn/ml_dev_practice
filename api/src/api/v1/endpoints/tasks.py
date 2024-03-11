from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from core.container import Container
from schema.task_schema import CreateTaskRequest, CreateTaskResponse, HistoryTaskResponse, HistoryTaskRequest
from services.task_service import TaskService
from model.user import User
from core.dependencies import get_current_active_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post("/", response_model=CreateTaskResponse)
@inject
async def create_task(request: CreateTaskRequest, service: TaskService = Depends(Provide[Container.task_service]), current_user: User = Depends(get_current_active_user)):
    return service.add(request, current_user)


@router.get("/history", response_model=HistoryTaskResponse)
@inject
async def tasks_history(service: TaskService = Depends(Provide[Container.task_service]), current_user: User = Depends(get_current_active_user)):
    request = HistoryTaskRequest()
    request.user_id = current_user.id
    return service.get_list(request)