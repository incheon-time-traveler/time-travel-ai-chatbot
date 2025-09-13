from fastapi import APIRouter, Query
from app.memory.locks import thread_lock, try_acquire_thread, release_thread
from app.memory.store import delete_thread, has_thread, find_thread, list_threads
from app.core.logging import get_logger

from typing import List

# 로거 생성
logger = get_logger(__name__)

router = APIRouter()

@router.delete("")
async def delete_memory(
    thread_id: str,
    force: bool = Query(False, description="실행 중이어도 강제 종료 후 삭제")
):
    logger.info(f"DELETE /memory API 호출: thread_id={thread_id}, force={force}")

    if not force:
        # delete_thread 함수 내부에서 이미 락을 사용한다. (이중 락킹 방지지)
        deleted = await delete_thread(thread_id)
        logger.info(f"메모리 삭제 완료 (일반모드): {deleted}행 삭제")
        return {"thread_id": thread_id, "deleted_rows": deleted, "complete": True}
    
    if await try_acquire_thread(thread_id, timeout=10):
        try:
            deleted = await delete_thread(thread_id)
            logger.info(f"메모리 삭제 완료 (강제모드): {deleted}행 삭제")
            return {"thread_id": thread_id, "deleted_rows": deleted, "forced":True, "complete": True}
        finally:
            release_thread(thread_id)
    else:
        # 락 획득 실패 시 적절한 에러 응답 반환
        logger.error(f"락 획득 실패: {thread_id}")
        return {"thread_id": thread_id, "error": "락 획득 실패", "forced":False, "complete": False}
    

@router.get("/exists")
async def thread_exists(thread_id: str):
    """
    해당 thread_id가 DB 어딘가에 존재하는지 여부만 반환
    """
    logger.info(f"GET /memory/exists API 호출: thread_id={thread_id}")
    exists = await has_thread(thread_id)
    logger.info(f"thread 존재 여부: {thread_id} -> {exists}")
    return {"thread_id": thread_id, "exists": exists}


@router.get("/locations")
async def thread_locations(thread_id: str):
    """
    thread_id가 들어있는 테이블과 건수 목록
    예: {"locations":[{"table":"checkpoints","count":3}, ...]}
    """
    logger.info(f"GET /memory/locations API 호출: thread_id={thread_id}")
    locs = await find_thread(thread_id)
    return {
        "thread_id": thread_id,
        "locations": [{"table": t, "count": c} for t, c in locs],
    }

@router.get("")
async def find_all_threads(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """
    DB에 저장된 thread_id 목록 (페이지네이션)
    - limit: 1 ~ 500
    - offset: 0부터
    """
    logger.info(f"GET /memory API 호출: limit={limit}, offset={offset}")
    items: List[str] = await list_threads(limit=limit, offset=offset)
    has_more = len(items) == limit
    next_offset = offset + limit if has_more else None
    logger.info(f"스레드 목록 반환: {len(items)}개")
    return {
        "items": items,
        "limit": limit,
        "offset": offset,
        "count": len(items),
        "has_more": has_more,
        "next_offset": next_offset,
    }