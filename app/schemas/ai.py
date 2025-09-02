from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    user_question: str
    user_id: str
    user_location: Optional[dict] = None    # {"lat": ~~, "lng": ~~}

class ChatResponse(BaseModel):
    ai_answer: str