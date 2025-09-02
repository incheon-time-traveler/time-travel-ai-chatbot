# app/services/ai_service.py
import asyncio
from uuid import uuid4

from app.services.graph_module import make_graph  # 내부 그래프 빌더
from app.schemas.ai import ChatRequest

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
    graph = await get_or_create_graph()
    if not req.user_question or not req.user_id:
        raise ValueError("user_question, user_id 파라미터가 필요합니다.")
    
    checkpoint_id = str(uuid4())
    config = {"configurable": {"thread_id": req.user_id, "checkpoint_id": checkpoint_id}}  # 대화 스레드 분리 (Django와 동일) :contentReference[oaicite:3]{index=3}

    # 메시지에 GPS를 실어 보내고 싶다면 additional_kwargs를 활용하도록
    # graph_module의 analyze 노드에 이미 훅이 있으니 옵션으로 붙여도 됨 :contentReference[oaicite:4]{index=4}
    # 여기서는 최소 이식: content만 전달
    result = await graph.ainvoke(
        {
            "messages": [
                {
                    "role": "user", 
                    "content": req.user_question,
                    "additional_kwargs": {
                        "user_lat": req.user_location.lat,
                        "user_lon": req.user_location.lng
                    }
                }
            ]
        }, config=config)
    return result["messages"][-1].content