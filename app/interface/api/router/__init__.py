from fastapi import APIRouter

from . import task_list

router = APIRouter(prefix="/api/v1")

router.include_router(task_list.router)
