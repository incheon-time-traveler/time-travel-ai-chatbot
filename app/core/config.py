from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # 기본 설정
    PROJECT_NAME: str = "AI Server"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS 설정
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 데이터베이스 설정
    DATABASE_URL: str = "sqlite:///./ai_server.db"
    
    # 보안 설정
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI 모델 설정
    AI_MODEL_PATH: Optional[str] = None
    AI_MODEL_CONFIG: dict = {}
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/ai_server.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 전역 설정 인스턴스
settings = Settings()

# 환경 변수에서 설정 로드
if os.path.exists(".env"):
    settings = Settings(_env_file=".env")
