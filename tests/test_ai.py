import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_text():
    """AI 텍스트 생성 API 테스트"""
    response = client.post(
        "/api/v1/ai/generate",
        json={
            "prompt": "안녕하세요",
            "model": "default",
            "max_tokens": 100,
            "temperature": 0.7
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "model" in data
    assert "tokens_used" in data
    assert "processing_time" in data

def test_get_models():
    """사용 가능한 모델 목록 API 테스트"""
    response = client.get("/api/v1/ai/models")
    
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) > 0

def test_ai_health():
    """AI 서비스 상태 확인 API 테스트"""
    response = client.get("/api/v1/ai/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ai"
