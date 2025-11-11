# 1. 베이스 이미지 (Python)
FROM python:3.11-slim

# 2. 작업 디렉토리 생성
WORKDIR /app

# 3. 시스템 패키지 설치 (Pillow 등 이미지 처리 시 필수)
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. requirements.txt 복사
COPY requirements.txt /app/

# 5. 파이썬 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6. 프로젝트 전체 복사
COPY . /app/

# 7. 장고 환경 변수
ENV PYTHONUNBUFFERED=1

# 8. 포트 노출
EXPOSE 8000

# 9. 장고 실행 명령
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
