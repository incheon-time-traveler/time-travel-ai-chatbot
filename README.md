# FastAPI AI Server

FastAPI를 사용하여 구축된 AI 서버 애플리케이션입니다.

## 🚀 주요 기능

- **AI 텍스트 생성**: 다양한 AI 모델을 통한 텍스트 생성
- **RESTful API**: 표준 REST API 엔드포인트 제공
- **자동 문서화**: Swagger UI를 통한 API 문서 자동 생성
- **로깅 시스템**: 체계적인 로깅 및 모니터링

## 📁 프로젝트 구조

```
time-travel-bot/
├── app/                           # 메인 애플리케이션 패키지
│   ├── api/                       # API 엔드포인트
│   │   └── v1/                    # API v1 버전
│   │       ├── endpoints/         # API 엔드포인트 구현
│   │       │   ├── ai.py
│   │       │   └── memory.py
│   │       └── routers.py         # API 라우터 통합
│   ├── core/                      # 핵심 설정 및 유틸리티
│   │   ├── config.py              # 애플리케이션 설정
│   │   └── logging.py             # 로깅 설정
│   ├── schemas/                   # 스키마 모음
│   │   └── ai.py
│   ├── services/                  # 비즈니스 로직 서비스
│   │   └── ai_service.py          # AI 서비스 로직
│   └── main.py                    # 애플리케이션 진입점
├── tests/                         # 테스트 코드
│   └── test_ai.py                 # AI API 테스트
├── logs/                          # 로그 파일 (자동 생성)
├── requirements.txt               # Python 의존성 패키지
├── Dockerfile             
├── docker-compose.yml
├── env.example                    # 환경 변수 설정 예시
└── README.md                      # 프로젝트 문서
```

## 🛠️ 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt

# 또는

pip install requests beautifulsoup4 langchain langchain-core langchain-community langchain-chroma langchain-huggingface langchain-tavily langchain-openai langchain-upstage langgraph sentence-transformers pyowm faiss-cpu langgraph-checkpoint-sqlite aiosqlite
```

### 2. 환경 변수 설정

```bash
# env.example을 .env로 복사하고 필요한 값들을 설정
cp env.example .env
```

### 3. 서버 실행

```bash
# 개발 모드로 실행
python -m app.main

# 또는 uv로 실행
uv run -m app.main

# 또는 uvicorn을 직접 사용
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. API 문서 확인

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔌 API 엔드포인트

### AI 관련
- `POST /v1/chatbot` - AI 텍스트 생성
- `POST /v1/chat` - AI 텍스트 생성 (stream)

## 🧪 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest tests/test_ai.py

# 상세한 출력과 함께 실행
pytest -v
```

## 🔧 개발 가이드

### 새로운 API 엔드포인트 추가

1. `app/api/v1/endpoints/` 디렉토리에 새로운 파일 생성
2. `app/api/v1/api.py`에 새 라우터 등록
3. 필요한 경우 `app/services/`에 비즈니스 로직 추가

### 환경 변수 추가

1. `app/core/config.py`의 `Settings` 클래스에 새 설정 추가
2. `env.example`에 예시 값 추가

## 📝 TODO

- [ ] 폴더 구조 최적화
- [ ] 배포 서버 안정화 확인

## 🤝 기여하기

1. 이 저장소를 Fork
2. 새로운 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 Push (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

