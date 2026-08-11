"""Normalização de códigos de disciplina e siglas de professor."""

from __future__ import annotations

import re

from ingest.models import GradeCell, GradeSnapshot

# Aliases comuns do OCR / Untis → código interno do solver
DISCIPLINA_ALIASES: dict[str, str] = {
    "port.": "port",
    "port": "port",
    "portugues": "port",
    "daf": "DaF",
    "deutsch": "DaF",
    "ing.": "ing",
    "english": "ing",
    "mat.": "mat",
    "matematica": "mat",
    "g.l.": "GL",
    "gl": "GL",
}


def normalize_disciplina(raw: str) -> str:
    key = raw.strip().lower()
    return DISCIPLINA_ALIASES.get(key, raw.strip())


def normalize_professor(raw: str) -> str:
    return re.sub(r"\s+", "", raw.strip())


def normalize_snapshot(snapshot: GradeSnapshot) -> GradeSnapshot:
    cells = [
        GradeCell(
            turma_codigo=c.turma_codigo,
            dia=c.dia,
            tempo=c.tempo,
            disciplina=normalize_disciplina(c.disciplina),
            professor=normalize_professor(c.professor),
        )
        for c in snapshot.cells
    ]
    return GradeSnapshot(
        cells=cells,
        source_format=snapshot.source_format,
        status=snapshot.status,
        warnings=list(snapshot.warnings),
        snapshot_id=snapshot.snapshot_id,
        semestre_id=snapshot.semestre_id,
        metadata={**snapshot.metadata, "normalized": True},
    )
