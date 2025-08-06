from fastapi import APIRouter

from . import task, task_list

router = APIRouter(prefix="/api/v1")

router.include_router(task_list.router)
router.include_router(task.router)
