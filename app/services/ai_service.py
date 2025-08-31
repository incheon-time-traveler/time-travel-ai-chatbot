# app/services/ai_service.py
from typing import Optional
import asyncio

from app.services.graph_module import make_graph  # 내부 그래프 빌더

_graph = None
_graph_lock = asyncio.Lock()

async def get_or_create_graph():
    global _graph
    if _graph is None:
        async with _graph_lock:
            if _graph is None:
                _graph = await make_graph()
    return _graph


async def ask_ai(user_question: str, user_id: str, user_lat: Optional[str] = None, user_lon: Optional[str] = None) -> str:
    """
    Django views.chat_with_bot와 동일한 계약: 마지막 AI 메시지를 content로 반환.
    """
    graph = await get_or_create_graph()
    if not user_question or not user_id:
        raise ValueError("user_question, user_id 파라미터가 필요합니다.")

    config = {"configurable": {"thread_id": user_id}}  # 대화 스레드 분리 (Django와 동일) :contentReference[oaicite:3]{index=3}

    # 메시지에 GPS를 실어 보내고 싶다면 additional_kwargs를 활용하도록
    # graph_module의 analyze 노드에 이미 훅이 있으니 옵션으로 붙여도 됨 :contentReference[oaicite:4]{index=4}
    # 여기서는 최소 이식: content만 전달
    result = await graph.ainvoke({"messages": [{"role": "user", "content": user_question}]}, config=config)
    return result["messages"][-1].content
