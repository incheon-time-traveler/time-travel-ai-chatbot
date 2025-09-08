# app/services/ai_service.py
import asyncio
from datetime import datetime, timezone, timedelta

from langchain_core.messages import HumanMessage, SystemMessage

from app.services.graph_module import make_graph  # 내부 그래프 빌더
from app.schemas.ai import ChatRequest
from app.core.logging import get_logger

# 로거 생성
logger = get_logger(__name__)

# 한국 시간
KST = timezone(timedelta(hours=9))

_graph = None
_graph_lock = asyncio.Lock()

async def get_or_create_graph():
    global _graph
    if _graph is None:
        async with _graph_lock:
            if _graph is None:
                _graph = await make_graph()
    return _graph


async def ask_ai(req: ChatRequest) -> str:
    """
    마지막 AI 메시지를 content로 반환.
    """
    logger.info(f"AI 요청 시작 - user_id: {req.user_id}, question: {req.user_question[:50]}...")

    try:
        graph = await get_or_create_graph()
        if not req.user_question or not req.user_id:
            raise ValueError("user_question, user_id 파라미터가 필요합니다.")
        
        config = {"configurable": {"thread_id": req.user_id}}

        new_message = HumanMessage(
            content=req.user_question,
            additional_kwargs={
                "user_lat": req.user_location.lat if req.user_location else None,
                "user_lon": req.user_location.lng if req.user_location else None
            }
        )

        system_message = SystemMessage(
            content=f"""
            오늘이나 현재 같은 표현 쓰면 아래의 현재 시간을 참고하세요.
            - 현재 시간: {datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')}
            """
        )

        # 메시지에 GPS를 실어 보내고 싶다면 additional_kwargs를 활용하도록
        # 여기서는 최소 이식: content만 전달
        result = await graph.ainvoke(
            {"messages": [system_message, new_message]},
            config=config
        )

        logger.info(f"AI 응답 완료 - user_id: {req.user_id}")
        return result["messages"][-1].content
    
    except Exception as e:
        logger.error(f"AI 서비스 오류 - user_id: {req.user_id}, error: {e}")
        raise