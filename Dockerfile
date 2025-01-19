FROM python:3.10-slim-bullseye

RUN useradd --create-home mtsi
RUN mkdir /mtsi/sat-images
WORKDIR /home/mtsi/sat-images
USER mtsi

COPY configs/ configs/
COPY src/ src/
COPY requirements.txt requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/home/mtsi/sat-images/src"
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt && pip cache purge

CMD [ "python", "src/main.py" ]