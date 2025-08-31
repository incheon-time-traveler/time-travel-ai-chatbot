# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.api.v1.api import api_v1_router
from app.api.v1.endpoints.ai import ChatRequest
from app.services.ai_service import get_or_create_graph
from app.core.config import settings

import json

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 배포시 도메인으로 제한 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# def warmup():
#     # 그래프 미리 로드(초기 지연 줄이기)
#     get_or_create_graph()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post(f"{settings.API_V1_STR}/chat")
async def answer(req: ChatRequest):
    async def event_stream():
        graph = await get_or_create_graph()
        config = {"configurable": {"thread_id": req.user_id}}
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
            # "X-Accel-Buffering": "no",
        })

app.include_router(api_v1_router, prefix=settings.API_V1_STR)
