FROM python:3.10-slim-bullseye

RUN useradd --create-home dem
RUN mkdir /home/dem/dem-images
WORKDIR /home/dem/dem-images
USER dem

COPY configs/ configs/
COPY src/ src/
COPY requirements.txt requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/home/dem/dem-images/src"
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt && pip cache purge

CMD [ "python", "src/main.py" ]