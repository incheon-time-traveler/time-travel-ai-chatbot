# tests/test_ai.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_missing_params():
    resp = client.post("/v1/chat", json={"user_question": "안녕"})
    assert resp.status_code == 422  # Pydantic 검증

def test_chat_ok(monkeypatch):
    def fake_ask_ai(q, uid, lat=None, lon=None): return "hi!"
    from app.services import ai_service
    monkeypatch.setattr(ai_service, "ask_ai", fake_ask_ai)

    resp = client.post("/v1/chat", json={"user_question":"안녕","user_id":"u1"})
    assert resp.status_code == 200
    assert resp.json()["ai_answer"] == "hi!"
