import logging
import os
from datetime import datetime
from app.core.config import settings

def setup_logging():
    """로깅 설정을 초기화합니다."""
    
    # 로그 디렉토리 생성
    log_dir = os.path.dirname(settings.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 로그 포맷 설정
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # 루트 로거 설정
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(settings.LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # 특정 라이브러리들의 로그 레벨 조정
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    # 로거 생성
    logger = logging.getLogger(__name__)
    logger.info("로깅 시스템이 초기화되었습니다.")
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """지정된 이름의 로거를 반환합니다."""
    return logging.getLogger(name)
