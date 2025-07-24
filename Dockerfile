# Sử dụng image nhẹ nhưng đầy đủ
FROM python:3.10-slim

# Tạo thư mục làm việc
WORKDIR /code

# Cài các thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements vào trước
COPY requirements.txt .

# Cài pip và công cụ build PEP 517 (đặc biệt là meson cho pycairo)
RUN pip install --upgrade pip setuptools wheel \
    && pip install meson meson-python

# Cài các thư viện Python từ requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ project vào
COPY . .

# Chạy app FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
