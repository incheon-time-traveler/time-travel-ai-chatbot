# app/api/v1/api.py
from fastapi import APIRouter
from app.api.v1.endpoints import ai, memory

api_v1_router = APIRouter()
api_v1_router.include_router(ai.router, prefix="")
api_v1_router.include_router(memory.router, prefix="/memory")
