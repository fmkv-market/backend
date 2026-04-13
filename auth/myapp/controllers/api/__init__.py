from fastapi import APIRouter
from myapp.controllers.api.email_auth import router as email_router

router = APIRouter(
    prefix="/auth"
)
router.include_router(email_router)