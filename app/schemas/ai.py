from pydantic import BaseModel
from typing import Optional

class UserLocation(BaseModel):
    lat: float
    lng: float

class ChatRequest(BaseModel):
    user_question: str
    user_id: str
    user_location: Optional[UserLocation] = None

class ChatResponse(BaseModel):
    ai_answer: str