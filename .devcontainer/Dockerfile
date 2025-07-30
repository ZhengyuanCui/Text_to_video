FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3 python3-pip git git-lfs ffmpeg wget curl \
    && git lfs install \
    && apt-get clean

WORKDIR /workspace

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install HuggingFace CLI (for model pulls)
RUN pip install huggingface_hub

# Copy backend code
COPY ./backend ./backend

EXPOSE 8000
