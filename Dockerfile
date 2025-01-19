FROM python:3.12-slim-bullseye

ARG USER_ID=1000
ARG GROUP_ID=1000

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g $GROUP_ID mtsi_group && \
    useradd -m -u $USER_ID -g mtsi_group mtsi_user

RUN mkdir -p /home/mtsi/sentinel_images/landing && \
    mkdir -p /home/mtsi/sat-images && \
    chown -R mtsi_user:mtsi_group /home/mtsi

USER mtsi_user

WORKDIR /home/mtsi/sat-images

COPY configs/ configs/
COPY src/ src/
COPY requirements.txt requirements.txt

ENV IMAGES_DIR=/home/mtsi/sentinel_images/landing
ENV PYTHONPATH="${PYTHONPATH}:/home/mtsi/sat-images/src"

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt && pip cache purge

CMD ["python", "src/main.py"]
