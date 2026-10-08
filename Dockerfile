
FROM python:3.13-slim

WORKDIR /app

COPY producer/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY producer/ ./producer/

ENV PYTHONUNBUFFERED=1
ENV PUBLISH_MODE=local

CMD ["python", "-m", "producer.run"]
