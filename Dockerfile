
FROM python:3.10-slim


WORKDIR /code


RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2-dev \
    libpangocairo-1.0-0 \      
    pkg-config \
    python3-dev \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*



COPY requirements.txt .


RUN pip install --upgrade pip setuptools wheel \
    && pip install meson meson-python


RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
