FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 설정
WORKDIR /chatbot

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 애플리케이션 전체 복사 (run.py 포함)
COPY . .

EXPOSE 8000

CMD [ "python", "run.py" ]

