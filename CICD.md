# CI/CD

## AWS EC2

1. EC2 인스턴스 생성

- t2.micro & 30GB 선택
- pem 키 생성
- 인바운드 그룹 생성
    - 사용자 TCP 설정

## Docker

1. Dockerfile + docker-compose.yml

- Dockerfile : 도커 이미지 생성용 파일
    - 도커 컨테이너 안의 환경을 설정한다

## ssh 연결

- docker, docker-compose 설치

```bash
# Docker 설치
# 1. 프로그램 설치 전 우분투 시스템 패키지 업데이트
$ sudo apt-get update
 
# 2. 필요한 패키지 설치
$ sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
 
# 3. Docker의 공식 GPG 키 추가
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
 
# 4. Docker의 공식 apt 저장소 추가
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# 5. 시스템 패키지 업데이트
$ sudo apt-get update
 
# 6. Docker 설치
$ sudo apt-get install docker-ce docker-ce-cli containerd.io

# Docker compose 설치
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 다운로드 한 파일에 권한 설정
$ sudo chmod +x /usr/local/bin/docker-compose
```

- 환경 설정에 필요한 것을 먼저 설치한다.
- git clone을 통해서 빌드할 프로젝트 폴더 내용을 넣어준다.
- .gitignore에 있던 파일 중 필요한 것을 직접 넣어준다.

## 빌드

```bash
sudo docker compose build && docker compose up -d

sudo docker compose ps

sudo docker compose logs -f
```

```bash
# 스택 정리(볼륨 보존)
sudo docker compose down --remove-orphans

# 미사용 리소스 정리
sudo docker system prune -a --volumes -f
sudo docker builder prune -a -f

# 최신 이미지/의존성 반영 + 캐시없이 재빌드
sudo docker compose pull
sudo docker compose build --no-cache --pull

# 재기동 및 로그 확인
sudo docker compose up -d
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

---

## 배포를 위한 수정 사항

### 1\. EC2 인스턴스에 적합한 모델인가 판단하기

- 원래 사용했던 모델은 `intfloat/multilingual-e5-large-instruct`이다.
    - 1.4GB 정도로 인스턴스에서 사용하기에는 무거웠음.

- 수정한 모델은 `dragonkue/multilingual-e5-small-ko-v2`이다.
    - 400MB~500MB 정도로 매우 작다.
    - 한국어 특화 (ko)
    - 다국어 지원 (multilingual)
    - 상대적으로 작은 크기 (400MB)
    - E5 시리즈 (높은 품질)