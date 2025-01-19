FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/mtsi/sentinel_images/landing

WORKDIR /home/mtsi/sat-images

COPY configs/ configs/
COPY src/ src/
COPY requirements.txt requirements.txt

ENV IMAGES_DIR=/home/mtsi/sentinel_images/landing
ENV PYTHONPATH="${PYTHONPATH}:/home/mtsi/sat-images/src"

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt && pip cache purge

CMD ["python", "src/main.py"]
