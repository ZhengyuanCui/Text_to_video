FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip git ffmpeg && apt-get clean
WORKDIR /app

COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt \
    && pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

COPY . .

ENV PYTHONPATH=/app
ENV REDIS_URL=redis://redis:6379/0
ENV ARTIFACT_DIR=/videos

# run api by default
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
