from fastapi import APIRouter

from myapp.controllers.api.profile import router as profile_router
from myapp.controllers.api.address import router as address_router

router = APIRouter(prefix="/api")
router.include_router(profile_router)
router.include_router(address_router)