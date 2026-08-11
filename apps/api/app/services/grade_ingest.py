"""Persistência de GradeSnapshot → ingest_snapshot + grade_celula."""

from __future__ import annotations

import os
import uuid
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.enums import IngestSnapshotStatus, IngestSourceFormat
from app.db.models import GradeCelula, Grupo, IngestSnapshot, Semestre, Turma

from ingest.checkin import load_legacy_py
from ingest.extract_pdf import extract_pdf
from ingest.extract_xlsx import extract_xlsx
from ingest.models import GradeSnapshot, IngestWarning
from ingest.normalize import normalize_snapshot
from ingest.validate import validate_snapshot


def _detect_format(filename: str) -> IngestSourceFormat:
    lower = filename.lower()
    if lower.endswith(".py"):
        return IngestSourceFormat.legacy_py
    if lower.endswith(".pdf"):
        return IngestSourceFormat.pdf
    if lower.endswith((".xlsx", ".xls")):
        return IngestSourceFormat.xlsx
    raise ValueError(f"formato não suportado: {filename}")


def extract_from_file(path: Path, source_format: IngestSourceFormat) -> GradeSnapshot:
    if source_format == IngestSourceFormat.legacy_py:
        snapshot = load_legacy_py(path)
    elif source_format == IngestSourceFormat.pdf:
        snapshot = extract_pdf(path)
    else:
        snapshot = extract_xlsx(path)
    snapshot = normalize_snapshot(snapshot)
    return validate_snapshot(snapshot)


def _get_or_create_import_grupo(db: Session, segmento_id: uuid.UUID) -> Grupo:
    grupo = db.scalar(
        select(Grupo).where(Grupo.segmento_id == segmento_id, Grupo.nome == "Importação grade")
    )
    if grupo:
        return grupo
    from datetime import date

    grupo = Grupo(
        segmento_id=segmento_id,
        nome="Importação grade",
        data_inicio_semestre=date(2026, 1, 1),
        data_fim_semestre=date(2026, 12, 31),
        datas_segunda_chamada=[],
        conselho_inicio=date(2026, 11, 1),
        conselho_fim=date(2026, 11, 30),
    )
    db.add(grupo)
    db.flush()
    return grupo


def _resolve_turma(db: Session, semestre: Semestre, codigo: str) -> Turma | None:
    turma = db.scalar(select(Turma).where(Turma.codigo == codigo))
    if turma:
        return turma
    grupo = _get_or_create_import_grupo(db, semestre.segmento_id)
    turma = Turma(grupo_id=grupo.id, codigo=codigo)
    db.add(turma)
    db.flush()
    return turma


def persist_snapshot(
    db: Session,
    semestre: Semestre,
    snapshot: GradeSnapshot,
    *,
    arquivo_entrada_id: uuid.UUID | None,
    source_format: IngestSourceFormat,
) -> tuple[IngestSnapshot, list[IngestWarning]]:
    extra_warnings: list[IngestWarning] = []
    ingest = IngestSnapshot(
        semestre_id=semestre.id,
        arquivo_entrada_id=arquivo_entrada_id,
        status=snapshot.status,
        source_format=source_format,
        warnings=[w.to_dict() for w in snapshot.warnings],
        metadata_=snapshot.metadata,
        checksum=snapshot.checksum(),
    )
    db.add(ingest)
    db.flush()

    for cell in snapshot.cells:
        turma = _resolve_turma(db, semestre, cell.turma_codigo)
        if turma is None:
            extra_warnings.append(
                IngestWarning(
                    code="TURMA_UNRESOLVED",
                    message=f"turma {cell.turma_codigo} não resolvida",
                    turma_codigo=cell.turma_codigo,
                    severity="critical",
                )
            )
            continue
        db.add(
            GradeCelula(
                ingest_snapshot_id=ingest.id,
                turma_id=turma.id,
                dia=cell.dia,
                tempo=cell.tempo,
                disciplina=cell.disciplina,
                professor=cell.professor,
            )
        )

    if extra_warnings:
        merged = [IngestWarning(**w) if isinstance(w, dict) else w for w in ingest.warnings]
        for w in extra_warnings:
            merged.append(w)
        ingest.warnings = [w.to_dict() if hasattr(w, "to_dict") else w for w in merged]
        ingest.status = IngestSnapshotStatus.pending_review

    db.commit()
    db.refresh(ingest)
    return ingest, extra_warnings


def approve_snapshot(db: Session, snapshot: IngestSnapshot) -> IngestSnapshot:
    warnings = snapshot.warnings or []
    critical = any(w.get("severity") == "critical" for w in warnings)
    if critical:
        raise ValueError("snapshot com avisos críticos não pode ser aprovado")
    snapshot.status = IngestSnapshotStatus.approved
    db.commit()
    db.refresh(snapshot)
    return snapshot
