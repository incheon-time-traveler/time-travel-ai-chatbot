# thread_id 단위 삭제/조회/통계
# aiosqlite 직접 접근
import os
import re
from typing import List, Tuple

import aiosqlite
from app.core.config import settings

MEMORY_DB = settings.MEMORY_DB
CANDIDATE_THREAD_COLS = ["thread_id", "parent_thread_id", "source_thread_id"]

def is_db_exists(db_path: str) -> bool:
    """파일 기반 DB가 실제로 존재하는지 확인(:memory:는 True로 간주 안 함)."""
    return db_path != ":memory:" and os.path.exists(db_path)

async def fetchone(db: aiosqlite.Connection, sql: str, params=()):
    async with db.execute(sql, params) as cur:
        return await cur.fetchone()

async def fetchall(db: aiosqlite.Connection, sql: str, params=()):
    async with db.execute(sql, params) as cur:
        return await cur.fetchall()

async def list_tables(db: aiosqlite.Connection) -> List[str]:
    rows = await db.execute_fetchall(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    return [r[0] for r in rows]

# 테이블이 해당 컬럼을 가지고있는지
async def table_has_column(db: aiosqlite.Connection, table: str, col: str) -> bool:
    cols = await fetchall(db, f"PRAGMA table_info({table});")
    return any(c[1] == col for c in cols)  # c[1] = column name


async def tables_with_any_of(
    db: aiosqlite.Connection, colnames: List[str]
) -> List[Tuple[str, List[str]]]:
    """
    주어진 컬럼명들 중 하나 이상을 포함하는 (table, hits) 목록.
    """
    hit: List[Tuple[str, List[str]]] = []
    tables = await list_tables(db)
    for t in tables:
        cols = await fetchall(db, f"PRAGMA table_info({t});")
        names = {c[1] for c in cols}
        hits = [c for c in colnames if c in names]
        if hits:
            hit.append((t, hits))
    return hit


# API 함수

async def delete_thread(thread_id: str) -> int:
    """
    지정 thread_id 관련 레코드를 모든 테이블에서 삭제.
    반환: 삭제된 행 수의 합(대략치).

    주의:
    - 파일이 아예 없으면 새 DB를 만들지 않도록 0을 반환하고 종료.
    - 삭제 후 WAL 체크포인트/ VACUUM로 공간 회수.
    """
    if MEMORY_DB == ":memory:":
        # 인메모리 DB는 프로세스 종료 시 전체 소멸
        return 0
    if not is_db_exists(MEMORY_DB):
        return 0
    
    deleted_total = 0
    async with aiosqlite.connect(MEMORY_DB) as db:
        await db.execute("PRAGMA foreign_keys=ON;")
        # thread id 관련 컬럼 후보 (버전에 따라 다를 수 있어 넉넉히 포함)
        candidate_cols = ["thread_id", "parent_thread_id", "source_thread_id"]

        targets = await tables_with_any_of(db, candidate_cols)
        for table, cols in targets:
            where = " OR ".join([f"{c} = ?" for c in cols])
            params = [thread_id] * len(cols)
            cur = await db.execute(f"DELETE FROM {table} WHERE {where};", params)
            deleted_total += int(cur.rowcount or 0)
            
        # WAL 체크포인트/공간 회수(선택이지만 권장)
        await db.execute("PRAGMA wal_checkpoint(TRUNCATE);")
        await db.execute("VACUUM;")
        await db.commit()

    return deleted_total


async def has_thread(thread_id: str) -> bool:
    """
    주어진 thread_id가 DB 어딘가에 '존재'하는지만 빠르게 확인.
    """
    if MEMORY_DB == ":memory:" or not is_db_exists(MEMORY_DB):
        return False

    async with aiosqlite.connect(MEMORY_DB) as db:
        targets = await tables_with_any_of(db, CANDIDATE_THREAD_COLS)
        for table, cols in targets:
            where = " OR ".join([f"{c} = ?" for c in cols])
            params = [thread_id] * len(cols)
            row = await fetchone(
                db, f"SELECT 1 FROM {table} WHERE {where} LIMIT 1;", params
            )
            if row is not None:
                return True
    return False


async def find_thread(thread_id: str) -> List[Tuple[str, int]]:
    """
    thread_id가 들어있는 테이블과 건수를 반환.
    예: [("checkpoints", 3), ("writes", 9)]
    """
    if MEMORY_DB == ":memory:" or not is_db_exists(MEMORY_DB):
        return []

    results: List[Tuple[str, int]] = []
    async with aiosqlite.connect(MEMORY_DB) as db:
        targets = await tables_with_any_of(db, CANDIDATE_THREAD_COLS)
        for table, cols in targets:
            where = " OR ".join([f"{c} = ?" for c in cols])
            params = [thread_id] * len(cols)
            row = await fetchone(
                db, f"SELECT COUNT(*) FROM {table} WHERE {where};", params
            )
            count = int(row[0]) if row else 0
            if count > 0:
                results.append((table, count))
    # 테이블명 기준 정렬(원하면 count desc로 바꿔도 됨)
    results.sort(key=lambda x: x[0])
    return results


# 스레드 목록 확인하기
async def list_threads(limit: int = 100, offset: int = 0) -> List[str]:
    if MEMORY_DB == ":memory:" or not is_db_exists(MEMORY_DB):
        return []

    async with aiosqlite.connect(MEMORY_DB) as db:
        tables = await list_tables(db)
        with_thread: List[str] = []
        for t in tables:
            if await table_has_column(db, t, "thread_id"):
                with_thread.append(t)

        if not with_thread:
            return []

        unions = " UNION ".join([f"SELECT thread_id FROM {t}" for t in with_thread])
        sql = f"""
            SELECT DISTINCT thread_id
            FROM ({unions})
            ORDER BY thread_id
            LIMIT ? OFFSET ?;
        """
        rows = await fetchall(db, sql, (limit, offset))
        return [r[0] for r in rows]