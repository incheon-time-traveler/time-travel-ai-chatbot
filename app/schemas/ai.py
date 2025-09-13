from pydantic import BaseModel
from typing import Optional

class UserLocation(BaseModel):
    lat: Optional[float] = None
    lng: Optional[float] = None


class UserInfo(BaseModel):
    nickname: Optional[str] = None
    gender : Optional[str] = None
    age_group: Optional[str] = None


class ChatRequest(BaseModel):
    user_question: str
    user_id: str
    user_location: Optional[UserLocation] = None
    user_info: Optional[UserInfo] = None
    

class ChatResponse(BaseModel):
    ai_answer: str