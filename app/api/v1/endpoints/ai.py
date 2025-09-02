# app/api/v1/endpoints/ai.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

import json
from uuid import uuid4

from app.services.ai_service import ask_ai
from app.services.ai_service import get_or_create_graph
from app.schemas.ai import ChatRequest, ChatResponse


router = APIRouter()

@router.post("/chatbot", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    챗봇이 답변을 한번에 제공함.
    """
    try:
        answer = await ask_ai(req)
        return ChatResponse(ai_answer=answer)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"챗봇 오류가 발생했습니다: {e}")

@router.post("/chat")
async def answer(req: ChatRequest):
    """
    챗봇이 답변을 stream으로 제공함.
    - checkpoint_id : 매 요청마다 uuid4()로 부여 (동시 런 충돌 완화)
    """
    checkpoint_id = str(uuid4())
    async def event_stream():
        graph = await get_or_create_graph()
        config = {"configurable": {"thread_id": req.user_id, "checkpoint_id": checkpoint_id}}
        try:
            async for chunk in graph.astream(
                input={
                    "messages": [
                        {
                            "role": "user",
                            "content": req.user_question,
                            "additional_kwargs": {
                                "user_lat": req.user_location["lat"],
                                "user_lon": req.user_location["lng"]
                            }
                        }
                    ]
                },
                config=config,
                stream_mode=["messages"]
            ):
                # ("messages", (AIMessageChunk, metadata))
                kind, payload = chunk
                if kind != "messages":
                    continue

                msg_chunk, meta = payload
                # 최종 노드만 통과
                if meta.get("langgraph_node") != "chatbot":
                    continue

                # 혹시 모를 중첩/예외 대비
                content = getattr(msg_chunk, "content", "")
                if not content:
                    continue

                # (선택) : JSON/에러 문구 차단
                if content.lstrip().startswith("{") or content.startswith("Error:"):
                    continue

                data = {"type": "delta", "content": content}
                print(f"data: {data}")
                yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

        except Exception as e:
            yield f"data: {str(e)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        })