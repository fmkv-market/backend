from fastapi import APIRouter

from myapp.controllers.api.item import router as item_router

router = APIRouter(prefix="/api/v1")
router.include_router(item_router)