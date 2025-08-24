# FastAPI AI Server

FastAPI를 사용하여 구축된 AI 서버 애플리케이션입니다.

## 🚀 주요 기능

- **AI 텍스트 생성**: 다양한 AI 모델을 통한 텍스트 생성
- **사용자 인증**: JWT 기반 사용자 인증 및 권한 관리
- **RESTful API**: 표준 REST API 엔드포인트 제공
- **자동 문서화**: Swagger UI를 통한 API 문서 자동 생성
- **로깅 시스템**: 체계적인 로깅 및 모니터링
- **데이터베이스 연동**: SQLAlchemy를 통한 데이터베이스 관리

## 📁 프로젝트 구조

```
time-travel-bot/
├── app/                    # 메인 애플리케이션 패키지
│   ├── api/               # API 엔드포인트
│   │   └── v1/           # API v1 버전
│   │       ├── endpoints/ # API 엔드포인트 구현
│   │       └── api.py     # API 라우터 통합
│   ├── core/              # 핵심 설정 및 유틸리티
│   │   ├── config.py      # 애플리케이션 설정
│   │   └── logging.py     # 로깅 설정
│   ├── database/          # 데이터베이스 관련
│   │   └── session.py     # 데이터베이스 세션 관리
│   ├── models/            # 데이터 모델
│   │   └── user.py        # 사용자 모델
│   ├── services/          # 비즈니스 로직 서비스
│   │   └── ai_service.py  # AI 서비스 로직
│   ├── utils/             # 유틸리티 함수
│   │   └── security.py    # 보안 관련 유틸리티
│   └── main.py            # 애플리케이션 진입점
├── tests/                 # 테스트 코드
│   └── test_ai.py         # AI API 테스트
├── logs/                  # 로그 파일 (자동 생성)
├── requirements.txt       # Python 의존성 패키지
├── env.example            # 환경 변수 설정 예시
└── README.md              # 프로젝트 문서
```

## 🛠️ 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
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

# 또는 uvicorn을 직접 사용
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. API 문서 확인

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔌 API 엔드포인트

### AI 관련
- `POST /api/v1/ai/generate` - AI 텍스트 생성
- `GET /api/v1/ai/models` - 사용 가능한 AI 모델 목록
- `GET /api/v1/ai/health` - AI 서비스 상태 확인

### 인증 관련
- `POST /api/v1/auth/register` - 사용자 등록
- `POST /api/v1/auth/login` - 사용자 로그인
- `POST /api/v1/auth/token` - OAuth2 토큰 발급
- `GET /api/v1/auth/me` - 현재 사용자 정보

### 사용자 관리
- `GET /api/v1/users/` - 사용자 목록 조회
- `GET /api/v1/users/{user_id}` - 특정 사용자 정보 조회
- `PUT /api/v1/users/{user_id}` - 사용자 정보 업데이트
- `DELETE /api/v1/users/{user_id}` - 사용자 삭제

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

### 새로운 데이터 모델 추가

1. `app/models/` 디렉토리에 새로운 모델 파일 생성
2. `app/database/session.py`의 `init_db()` 함수에 모델 import 추가

### 환경 변수 추가

1. `app/core/config.py`의 `Settings` 클래스에 새 설정 추가
2. `env.example`에 예시 값 추가

## 📝 TODO

- [ ] 실제 AI 모델 연동 (OpenAI, Hugging Face 등)
- [ ] 데이터베이스 마이그레이션 (Alembic)
- [ ] 사용자 권한 관리 시스템
- [ ] API 요청/응답 캐싱
- [ ] 모니터링 및 메트릭 수집
- [ ] Docker 컨테이너화
- [ ] CI/CD 파이프라인 구축

## 🤝 기여하기

1. 이 저장소를 Fork
2. 새로운 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 Push (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

