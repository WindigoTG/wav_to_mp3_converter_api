FROM python:3.10-slim

RUN mkdir /app

COPY requirements.txt /app

RUN python -m pip install -r /app/requirements.txt

RUN apt-get update && apt-get install -y \
    ffmpeg libavcodec-extra

#RUN apt-get install libav-tools libavcodec-extra

#RUN apt-get install ffmpeg libavcodec-extra

COPY wav_to_mp3 /app/wav_to_mp3

ENV PYTHONPATH "PYTHONPATH:/app"

WORKDIR /app/wav_to_mp3

CMD uvicorn main:app --host 0.0.0.0 --port 5000