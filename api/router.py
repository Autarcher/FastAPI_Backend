from fastapi import APIRouter
from api.v1 import exampleRouter

router = APIRouter(prefix="/lya/api")
router.include_router(exampleRouter)
