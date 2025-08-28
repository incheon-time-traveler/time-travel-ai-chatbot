from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # 기본 설정
    PROJECT_NAME: str = "TimeTravel Bot API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/v1"
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS 설정
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # AI 모델 설정
    AI_MODEL_PATH: Optional[str] = None
    AI_MODEL_CONFIG: dict = {}
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # API 키
    OPENAI_API_KEY: Optional[str] = None
    UPSTAGE_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None
    TAVILY_API_KEY: Optional[str] = None
    OPENWEATHERMAP_API_KEY: Optional[str] = None
    KAKAO_REST_API_KEY: Optional[str] = None

    # URL
    KAKAO_URL: Optional[str] = None
    KAKAO_MAP_URL: Optional[str] = None

    # DATA
    DB_PATH: Optional[str] = None
    RESTROOM_CSV: Optional[str] = None

    # 임베딩 모델
    EMBEDDING_MODEL: Optional[str] = None

    # user agent
    USER_AGENT: Optional[str] = None


    class Config:
        env_file = ".env"
        case_sensitive = True

# 전역 설정 인스턴스
settings = Settings()

# 환경 변수에서 설정 로드
if os.path.exists(".env"):
    settings = Settings(_env_file=".env")

