# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.memory.manager import aclose_checkpointer, ensure_checkpointer
from app.api.v1.routers import api_v1_router
from app.core.config import settings
from app.core.logging import setup_logging

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ready = False

    # 로깅 초기화
    logger = setup_logging()
    logger.info("애플리케이션이 시작됩니다.")

    try:
        await ensure_checkpointer()
        app.state.ready = True
        logger.info("애플리케이션이 준비되었습니다.")
        yield
    except Exception as e:
        logger.error(f"애플리케이션 시작 중 오류가 발생: {e}")
        raise
    finally:
        logger.info("애플리케이션이 종료됩니다.")
        await aclose_checkpointer()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 배포시 도메인으로 제한 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    return {"status": "ready" if getattr(app.state, "ready", False) else "starting"}

app.include_router(api_v1_router, prefix=settings.API_V1_STR)
