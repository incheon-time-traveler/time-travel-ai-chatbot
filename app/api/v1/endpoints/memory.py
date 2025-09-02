from fastapi import APIRouter, Query
from app.memory.locks import thread_lock
from app.memory.store import delete_thread, has_thread, find_thread, list_threads

from typing import List

router = APIRouter()

@router.delete("")
async def delete_memory(thread_id: str):
    try:
        async with thread_lock(thread_id):
            deleted = await delete_thread(thread_id)
        return {"user_id": thread_id, "deleted_rows": deleted}
    # 에러 찾기
    except Exception as e:
        return {"errer": str(e)}
    
@router.get("/exists")
async def thread_exists(thread_id: str):
    """
    해당 thread_id가 DB 어딘가에 존재하는지 여부만 반환
    """
    exists = await has_thread(thread_id)
    return {"thread_id": thread_id, "exists": exists}


@router.get("/locations")
async def thread_locations(thread_id: str):
    """
    thread_id가 들어있는 테이블과 건수 목록
    예: {"locations":[{"table":"checkpoints","count":3}, ...]}
    """
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
    items: List[str] = await list_threads(limit=limit, offset=offset)
    has_more = len(items) == limit
    next_offset = offset + limit if has_more else None
    return {
        "items": items,
        "limit": limit,
        "offset": offset,
        "count": len(items),
        "has_more": has_more,
        "next_offset": next_offset,
    }