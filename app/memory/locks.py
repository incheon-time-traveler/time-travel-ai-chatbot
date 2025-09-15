# user_id/thread_id 별 asyncio.Lock 제공
# 옵션 : 직렬화

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Optional

from app.core.logging import get_logger

# 로거 생성
logger = get_logger(__name__)

# 단일 워커 (프로세스) 전제에서, 키별 asyncio.Lock을 보관하는 저장소
lock_store: Dict[str, asyncio.Lock] = {}

def thread_key(thread_id: int) -> str:
    """내부 저장소에서 사용할 네임스페이스가 붙은 키"""
    if not thread_id:
        raise ValueError("thread_id required")
    return f"thread:{thread_id}"


def get_lock(key: str) -> asyncio.Lock:
    """키에 해당하는 락을 반환(없으면 생성)."""
    lock = lock_store.get(key)
    if lock is None:
        lock = asyncio.Lock()
        lock_store[key] = lock
    return lock


@asynccontextmanager
async def thread_lock(thread_id: int) -> AsyncIterator[None]:
    """
    동일 thread_id의 동시 실행을 1개로 제한(직렬화)하는 컨텍스트 매니저.
    사용 예:
        async with thread_lock(thread_id):
            async for chunk in graph.astream(...):
    """
    logger.debug(f"thread_lock 요청: {thread_id}")
    key = thread_key(thread_id)
    lock = get_lock(key)

    logger.debug(f"락 획득 시도: {thread_id}")
    await lock.acquire()
    try:
        logger.info(f"락 획득 성공: {thread_id}")
        yield
    finally:
        # 소유 태스크만 release 하기
        lock.release()
        logger.debug(f"락 해제: {thread_id}")


async def try_acquire_thread(thread_id: int, timeout: Optional[float] = None) -> bool:
    """
    thread_id 락을 시도해서 획득.
    - timeout is None 또는 0 : 즉시 시도(논 블로킹). 이미 잠겨있으면 False.
    - timeout > 0 : 지정 시간만큼 대기해서 획득 시 True, 타임이웃이면 False.
    사용 후에는 반드시 release_thread(thread_id)로 해제해야 함.
    """
    logger.debug(f"try_acquire_thread 호출: thread_id={thread_id}, timeout={timeout}")
    key = thread_key(thread_id)
    lock = get_lock(key)

    if timeout in (None, 0):
        if lock.locked():
            logger.debug(f"락이 이미 점유됨 (즉시 시도): {thread_id}")
            return False

        await lock.acquire()
        logger.info(f"락 획득 성공 (즉시 시도): {thread_id}")
        return True
    
    try:
        await asyncio.wait_for(lock.acquire(), timeout=timeout)
        logger.info(f"락 획득 성공 (타임아웃 {timeout}초): {thread_id}")
        return True
    except asyncio.TimeoutError:
        logger.warning(f"락 획득 타임아웃: {thread_id} (timeout={timeout}초)")
        return False
    

def release_thread(thread_id: int) -> None:
    """
    try_acquire_thread로 획득한 락을 해제.
    주의: 락의 소유 태스크에서만 호출해야 함.
    """
    logger.debug(f"release_thread 호출: {thread_id}")
    key = thread_key(thread_id)
    lock = lock_store.get(key)

    if lock and lock.locked():
        lock.release()
        logger.info(f"락 해제: {thread_id}")
    else:
        logger.warning(f"해제할 락이 없거나 이미 해제됨: {thread_id}")