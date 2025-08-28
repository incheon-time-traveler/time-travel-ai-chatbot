# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_v1_router
from app.services.ai_service import get_or_create_graph
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 배포시 도메인으로 제한 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def warmup():
    # 그래프 미리 로드(초기 지연 줄이기)
    get_or_create_graph()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(api_v1_router, prefix=settings.API_V1_STR)
