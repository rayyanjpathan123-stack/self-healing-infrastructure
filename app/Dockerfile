FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir ansible-core docker

RUN ansible-galaxy collection install community.docker

WORKDIR /app

COPY app/webhook.py /app/webhook.py

EXPOSE 5000

CMD ["python", "/app/webhook.py"]
