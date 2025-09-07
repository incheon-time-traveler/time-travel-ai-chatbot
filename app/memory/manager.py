# 체크포인터 생명주기
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from contextlib import AsyncExitStack
import asyncio

from app.core.config import settings
from app.core.logging import get_logger

# 로거 생성
logger = get_logger(__name__)

# 사용자 채팅 로그 저장하는 sqlite 경로
MEMORY_DB = settings.MEMORY_DB

# 여러 개의 비동기 컨텍스트 매니저를 한 곳에 모아 관리(열고 닫는)하는 스택
async_exit_stack = AsyncExitStack()
CHECKPOINTER = None
init_lock = asyncio.Lock()    # 체크 포인터 초기화 레이스 방지 락

# 체크포인트 열기
async def ensure_checkpointer():
    logger.info("체크포인터 초기화 시작")

    global CHECKPOINTER

    if CHECKPOINTER is not None:
        return CHECKPOINTER

    async with init_lock:    # 초기화 레이스 방지
        if CHECKPOINTER is None:    # double-checked
            try:
                # Async 컨텍스트 (체크포인터)를 열어서 스택에 등록
                # db_path = to_sqlite_uri(MEMORY_DB)
                CHECKPOINTER = await async_exit_stack.enter_async_context(
                    AsyncSqliteSaver.from_conn_string(MEMORY_DB)
                )
                logger.info("체크포인터 초기화 완료")
            except Exception as e:
                logger.error(f"체크포인터 초기화 실패: {e}")
                raise

    return CHECKPOINTER


# 체크포인트 닫기
async def aclose_checkpointer():
    await async_exit_stack.aclose()