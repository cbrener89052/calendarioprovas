"""Armazenamento local de blobs (S3/MinIO em produção futura)."""

from __future__ import annotations

import hashlib
import os
import uuid
from pathlib import Path

BLOB_ROOT = Path(os.getenv("BLOB_ROOT", "/tmp/calendarioprovas-blobs"))


def ensure_root() -> Path:
    BLOB_ROOT.mkdir(parents=True, exist_ok=True)
    return BLOB_ROOT


def save_bytes(data: bytes, *, prefix: str, filename: str) -> tuple[str, str]:
    """Retorna (blob_path relativo, sha256 hex)."""
    ensure_root()
    digest = hashlib.sha256(data).hexdigest()
    rel = f"{prefix}/{uuid.uuid4().hex}_{filename}"
    path = BLOB_ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return rel, digest


def read_bytes(blob_path: str) -> bytes:
    path = BLOB_ROOT / blob_path
    if not path.is_file():
        raise FileNotFoundError(blob_path)
    return path.read_bytes()
