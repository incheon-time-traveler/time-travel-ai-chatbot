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