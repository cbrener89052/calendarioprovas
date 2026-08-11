from __future__ import annotations

import tempfile
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.enums import ArquivoTipo, IngestSnapshotStatus
from app.db.models import ArquivoEntrada, GradeCelula, IngestSnapshot, Semestre
from app.schemas.ingest import IngestRunResponse, IngestSnapshotOut
from app.services.blob_storage import read_bytes
from app.services.grade_ingest import approve_snapshot, extract_from_file, persist_snapshot, _detect_format

router = APIRouter(tags=["ingest"])


def _snapshot_out(db: Session, snap: IngestSnapshot) -> IngestSnapshotOut:
    count = db.scalar(
        select(func.count()).select_from(GradeCelula).where(
            GradeCelula.ingest_snapshot_id == snap.id
        )
    )
    return IngestSnapshotOut(
        id=snap.id,
        semestre_id=snap.semestre_id,
        arquivo_entrada_id=snap.arquivo_entrada_id,
        status=snap.status.value,
        source_format=snap.source_format.value,
        checksum=snap.checksum,
        warnings=snap.warnings or [],
        metadata=snap.metadata_ or {},
        extracted_at=snap.extracted_at,
        approved_at=snap.approved_at,
        cell_count=int(count or 0),
    )


@router.post("/semestres/{semestre_id}/ingest/grade", response_model=IngestRunResponse)
def run_grade_ingest(
    semestre_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> IngestRunResponse:
    """Extrai grade do upload `grade` mais recente e persiste snapshot."""
    semestre = db.get(Semestre, semestre_id)
    if semestre is None:
        raise HTTPException(status_code=404, detail="semestre não encontrado")

    arquivo = db.scalar(
        select(ArquivoEntrada).where(
            ArquivoEntrada.semestre_id == semestre_id,
            ArquivoEntrada.tipo == ArquivoTipo.grade,
        )
    )
    if arquivo is None:
        raise HTTPException(status_code=404, detail="upload grade não encontrado — faça POST upload/grade primeiro")

    try:
        source_format = _detect_format(Path(arquivo.blob_path).name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    data = read_bytes(arquivo.blob_path)
    suffix = Path(arquivo.blob_path).suffix or ".bin"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)

    try:
        snapshot = extract_from_file(tmp_path, source_format)
        ingest, _extra = persist_snapshot(
            db,
            semestre,
            snapshot,
            arquivo_entrada_id=arquivo.id,
            source_format=source_format,
        )
    finally:
        tmp_path.unlink(missing_ok=True)

    cell_count = db.scalar(
        select(func.count()).select_from(GradeCelula).where(
            GradeCelula.ingest_snapshot_id == ingest.id
        )
    )
    return IngestRunResponse(
        snapshot_id=ingest.id,
        status=ingest.status.value,
        source_format=ingest.source_format.value,
        checksum=ingest.checksum,
        cell_count=int(cell_count or 0),
        warnings=ingest.warnings or [],
    )


@router.get("/semestres/{semestre_id}/ingest-snapshots", response_model=list[IngestSnapshotOut])
def list_ingest_snapshots(
    semestre_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> list[IngestSnapshotOut]:
    if db.get(Semestre, semestre_id) is None:
        raise HTTPException(status_code=404, detail="semestre não encontrado")
    snaps = db.scalars(
        select(IngestSnapshot)
        .where(IngestSnapshot.semestre_id == semestre_id)
        .order_by(IngestSnapshot.extracted_at.desc())
    ).all()
    return [_snapshot_out(db, s) for s in snaps]


@router.get("/ingest-snapshots/{snapshot_id}", response_model=IngestSnapshotOut)
def get_ingest_snapshot(
    snapshot_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> IngestSnapshotOut:
    snap = db.get(IngestSnapshot, snapshot_id)
    if snap is None:
        raise HTTPException(status_code=404, detail="snapshot não encontrado")
    return _snapshot_out(db, snap)


@router.post("/ingest-snapshots/{snapshot_id}/approve", response_model=IngestSnapshotOut)
def approve_ingest_snapshot(
    snapshot_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> IngestSnapshotOut:
    snap = db.get(IngestSnapshot, snapshot_id)
    if snap is None:
        raise HTTPException(status_code=404, detail="snapshot não encontrado")
    if snap.status == IngestSnapshotStatus.approved:
        return _snapshot_out(db, snap)
    try:
        snap = approve_snapshot(db, snap)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _snapshot_out(db, snap)
