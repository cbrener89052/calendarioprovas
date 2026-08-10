"""Extração de grade a partir de planilha xlsx (export Untis alternativo)."""

from __future__ import annotations

from pathlib import Path

from ingest.models import GradeSnapshot, IngestSourceFormat, IngestWarning


def extract_xlsx(path: str | Path) -> GradeSnapshot:
    """T3c: esqueleto — parsing xlsx será alinhado a extrair_grade_1semestre.py."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    warnings = [
        IngestWarning(
            code="NOT_IMPLEMENTED",
            message=f"extract_xlsx ainda não implementado para {path.name}",
            severity="critical",
        )
    ]
    return GradeSnapshot(
        cells=[],
        source_format=IngestSourceFormat.xlsx,
        warnings=warnings,
        metadata={"path": str(path)},
    )
