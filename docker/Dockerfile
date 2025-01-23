FROM python:3.11-slim

WORKDIR /opt/app
COPY requirements.txt ./

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y git
RUN python -m pip install --no-cache-dir -r requirements.txt \
    build \
    twine
