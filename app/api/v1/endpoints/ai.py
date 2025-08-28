# app/api/v1/endpoints/ai.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.ai_service import ask_ai

router = APIRouter()

class ChatRequest(BaseModel):
    user_question: str
    user_id: str
    user_lat: Optional[str] = None
    user_lon: Optional[str] = None

class ChatResponse(BaseModel):
    ai_answer: str

@router.post("/chatbot", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        answer = ask_ai(req.user_question, req.user_id, req.user_lat, req.user_lon)
        return ChatResponse(ai_answer=answer)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"챗봇 오류가 발생했습니다: {e}")
