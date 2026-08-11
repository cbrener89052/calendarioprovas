FROM python:3.11-slim

WORKDIR /app

COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/api/app ./app
COPY apps/api/alembic ./alembic
COPY apps/api/alembic.ini .
COPY apps/api/scripts ./scripts
COPY packages/ingest /packages/ingest

ENV PYTHONPATH=/packages/ingest
ENV BLOB_ROOT=/data/blobs

RUN mkdir -p /data/blobs

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
