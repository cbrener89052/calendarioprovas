from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class UploadResponse(BaseModel):
    arquivo_id: uuid.UUID
    tipo: str
    blob_path: str
    checksum: str


class IngestRunResponse(BaseModel):
    snapshot_id: uuid.UUID
    status: str
    source_format: str
    checksum: str
    cell_count: int
    warnings: list[dict[str, Any]]


class IngestSnapshotOut(BaseModel):
    id: uuid.UUID
    semestre_id: uuid.UUID
    arquivo_entrada_id: uuid.UUID | None
    status: str
    source_format: str
    checksum: str
    warnings: list[dict[str, Any]]
    metadata: dict[str, Any]
    extracted_at: datetime
    approved_at: datetime | None
    cell_count: int
