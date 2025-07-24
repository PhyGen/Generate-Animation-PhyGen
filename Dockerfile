FROM python:3.10-slim

WORKDIR /code

# Cài các thư viện hệ thống cần cho manim, pix2text, pycairo
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg \
    pkg-config \
    cmake \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Nâng pip và cài nhanh hơn với các tùy chọn tắt dependency resolver
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir --no-build-isolation --prefer-binary -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
