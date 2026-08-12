FROM python:3.11-slim

WORKDIR /app

COPY apps/worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/worker/worker ./worker
COPY packages/solver /packages/solver
COPY packages/ingest /packages/ingest
COPY gerar_calendario.py verificar_calendario.py /legacy/
COPY Klausurplan_2026_2SEM.xlsx /legacy/

ENV PYTHONPATH=/packages/solver:/packages/ingest:/legacy
ENV BLOB_ROOT=/data/blobs

RUN mkdir -p /data/blobs

CMD ["python", "-m", "worker.main"]
