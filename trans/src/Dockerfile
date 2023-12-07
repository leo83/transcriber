FROM python:3.10.13-slim-bookworm
RUN mkdir /trans
RUN mkdir trans/tmp
RUN mkdir -p /trans/models/whispercpp
COPY models/whispercpp/* /trans/models/whispercpp/
RUN apt update && apt upgrade 
RUN apt install -y ffmpeg
WORKDIR /trans
COPY requirements.txt /trans/
RUN pip install -r requirements.txt
COPY *.py /trans/
CMD uvicorn transcribe:app --host 0.0.0.0