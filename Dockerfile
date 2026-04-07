# 경량화된 파이썬 공식 이미지를 베이스로 사용합니다.
FROM python:3.10-slim-bullseye

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치 (만약 OpenCV나 EasyOCR 같은 라이브러리를 쓰신다면 필요한 시스템 패키지들)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt만 먼저 복사하여 캐시를 활용 (의존성 패키지가 변경되지 않았다면 캐시된 레이어 사용)
COPY requirements.txt .

# 파이썬 의존성 패키지 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션의 나머지 소스 코드를 복사 
COPY . .

# 포트 노출 (FastAPI 기본 포트 8000)
EXPOSE 8000

# 컨테이너 실행 시 uvicorn을 사용하여 서버 구동
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
