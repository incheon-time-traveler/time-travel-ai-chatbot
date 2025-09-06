# CI/CD

## AWS EC2

1. EC2 인스턴스 생성

## Docker

1. Dockerfile + docker-compose.yml

- Dockerfile : 도커 이미지 생성용 파일
    - 도커 컨테이너 안의 환경을 설정한다

## ssh 연결

- docker, docker-compose 설치
- 환경 설정에 필요한 것을 먼저 설치한다.
- git clone을 통해서 빌드할 프로젝트 폴더 내용을 넣어준다.
- .gitignore에 있던 파일 중 필요한 것을 직접 넣어준다.

## 빌드

```bash
sudo docker compose build && docker compose up -d

sudo docker compose ps

sudo docker compose logs -f
```

## HTTPS 관련

- 인증서를 받아야 함.
- nginx 사용

## 배포 환경에서 로그로 알 수 있는 문제들

### 1. **서버 상태 문제**
```
→ 서버 시작 실패, 메모리 시스템 문제
```

### 2. **API 요청/응답 문제**
```
2024-01-15 10:35:22 - app.api.v1.endpoints.ai - INFO - AI 요청 시작: user_id=123, query="화장실 찾기"
2024-01-15 10:35:25 - app.api.v1.endpoints.ai - ERROR - AI 서비스 호출 실패: API rate limit exceeded
```
→ API 호출 실패, 레이트 리미트, 네트워크 문제

### 3. **성능 문제**
```
2024-01-15 10:40:15 - app.services.ai_service - INFO - AI 응답 시간: 2.3초
2024-01-15 10:40:18 - app.services.ai_service - WARNING - AI 응답 시간이 5초를 초과: 6.2초
```
→ 응답 지연, 성능 저하

### 4. **데이터베이스 문제**
```
2024-01-15 10:45:10 - app.memory.store - ERROR - 메모리 저장 실패: Database connection lost
2024-01-15 10:45:12 - app.memory.store - WARNING - 메모리 로드 실패, 기본값 사용
```
→ DB 연결 문제, 데이터 손실

### 5. **외부 API 문제**
```
2024-01-15 10:50:15 - app.services.tool_module - ERROR - 카카오 API 호출 실패: 500 Internal Server Error
2024-01-15 10:50:16 - app.services.tool_module - WARNING - 대체 API 사용: 네이버 지도 API
```
→ 외부 서비스 장애, 대체 로직 동작

### 배포 환경에서 로그 활용 방법

1. **로그 파일 모니터링**: `logs/app.log` 파일을 실시간으로 모니터링
2. **에러 알림**: ERROR 레벨 로그 발생 시 알림 설정
3. **성능 모니터링**: 응답 시간, 메모리 사용량 등 추적
4. **사용자 행동 분석**: 어떤 기능이 많이 사용되는지, 어디서 에러가 발생하는지
