from fastapi import APIRouter
from .gost import gost_router

router = APIRouter()

router.include_router(gost_router)