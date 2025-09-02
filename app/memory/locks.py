# user_id/thread_id 별 asyncio.Lock 제공
# 옵션 : 직렬화

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Optional

# 단일 워커 (프로세스) 전제에서, 키별 asyncio.Lock을 보관하는 저장소
lock_store: Dict[str, asyncio.Lock] = {}

def thread_key(thread_id: str) -> str:
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
async def thread_lock(thread_id: str) -> AsyncIterator[None]:
    """
    동일 thread_id의 동시 실행을 1개로 제한(직렬화)하는 컨텍스트 매니저.
    사용 예:
        async with thread_lock(thread_id):
            async for chunk in graph.astream(...):
    """
    key = thread_key(thread_id)
    lock = get_lock(key)
    await lock.acquire()
    try:
        yield
    finally:
        # 소유 태스크만 release 하기
        lock.release()


def thread_locked(thread_id: str) -> bool:
    """해당 thread_id 락이 현재 점유 중인지 확인."""
    key = thread_key(thread_id)
    lock = lock_store.get(key)
    return bool(lock and lock.locked())


async def try_acquire_thread(thread_id: str, timeout: Optional[float] = None) -> bool:
    """
    thread_id 락을 시도해서 획득.
    - timeout is None 또는 0 : 즉시 시도(논 블로킹). 이미 잠겨있으면 False.
    - timeout > 0 : 지정 시간만큼 대기해서 획득 시 True, 타임이웃이면 False.
    사용 후에는 반드시 release_thread(thread_id)로 해제해야 함.
    """
    key = thread_key(thread_id)
    lock = get_lock(key)

    if timeout in (None, 0):
        if lock.locked():
            return False
        await lock.acquire()
        return True
    
    try:
        await asyncio.wait_for(lock.acquire(), timeout=timeout)
        return True
    except asyncio.TimeoutError:
        return False
    

def release_thread(thread_id: str) -> None:
    """
    try_acquire_thread로 획득한 락을 해제.
    주의: 락의 소유 태스크에서만 호출해야 함.
    """
    key = thread_key(thread_id)
    lock = lock_store.get(key)
    if lock and lock.locked():
        lock.release()


def cleanup_thread_lock(thread_id: str) -> bool:
    """
    해당 thread_id의 락이 사용 중이 아니면 lock_store에서 제거(메모리 정리).
    제거에 성공하면 True, 잠겨 있으면 False.
    """
    key = thread_key(thread_id)
    lock = lock_store.get(key)
    if lock and not lock.locked():
        del lock_store[key]
        return True
    return False

cancel_store: Dict[str, asyncio.Event] = {}

def get_cancel_event(thread_id: str) -> asyncio.Event:
    key = thread_key(thread_id)
    evt = cancel_store.get(key)
    if evt is None:
        evt = asyncio.Event()
        cancel_store[key] = evt
    return evt

def request_cancel(thread_id: str) -> None:
    """해당 thread_id의 실행 루프에게 '중단' 신호를 보냄"""
    get_cancel_event(thread_id).set()

def clear_cancel(thread_id: str) -> None:
    """다음 실행을 위해 취소 플래그를 초기화"""
    key = thread_key(thread_id)
    evt = cancel_store.get(key)
    if evt:
        evt.clear()

async def wait_until_unlocked(thread_id: str, timeout: float = 5.0) -> bool:
    """락이 풀릴 때까지 최대 timeout초 대기"""
    key = thread_key(thread_id)
    lock = lock_store.get(key)
    if not lock or not lock.locked():
        return True
    loop = asyncio.get_event_loop()
    deadline = loop.time() + timeout
    while lock.locked() and loop.time() < deadline:
        await asyncio.sleep(0.05)
    return not lock.locked()