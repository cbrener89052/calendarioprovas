"""Contrato compartilhado entre ingest, API e solver."""

from __future__ import annotations

import enum
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


class IngestSnapshotStatus(str, enum.Enum):
    draft = "draft"
    pending_review = "pending_review"
    approved = "approved"
    rejected = "rejected"


class IngestSourceFormat(str, enum.Enum):
    pdf = "pdf"
    xlsx = "xlsx"
    legacy_py = "legacy_py"


@dataclass(frozen=True)
class GradeCell:
    turma_codigo: str
    dia: int
    tempo: int
    disciplina: str
    professor: str

    def __post_init__(self) -> None:
        if not 1 <= self.dia <= 5:
            raise ValueError(f"dia fora do intervalo 1-5: {self.dia}")
        if not 1 <= self.tempo <= 13:
            raise ValueError(f"tempo fora do intervalo 1-13: {self.tempo}")


@dataclass(frozen=True)
class IngestWarning:
    code: str
    message: str
    turma_codigo: str | None = None
    dia: int | None = None
    tempo: int | None = None
    severity: str = "warning"  # info | warning | critical

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "turma_codigo": self.turma_codigo,
            "dia": self.dia,
            "tempo": self.tempo,
            "severity": self.severity,
        }


@dataclass
class GradeSnapshot:
    """Snapshot de grade extraída; imutável após aprovação."""

    cells: list[GradeCell]
    source_format: IngestSourceFormat
    status: IngestSnapshotStatus = IngestSnapshotStatus.draft
    warnings: list[IngestWarning] = field(default_factory=list)
    snapshot_id: str | None = None
    semestre_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def checksum(self) -> str:
        payload = sorted(
            [
                {
                    "turma": c.turma_codigo,
                    "dia": c.dia,
                    "tempo": c.tempo,
                    "disciplina": c.disciplina,
                    "professor": c.professor,
                }
                for c in self.cells
            ],
            key=lambda x: (x["turma"], x["dia"], x["tempo"]),
        )
        raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(raw.encode()).hexdigest()

    def to_grades_dict(self) -> dict[str, dict[tuple[int, int], tuple[str, str]]]:
        """Formato legado GRADES usado por gerar_calendario.py."""
        out: dict[str, dict[tuple[int, int], tuple[str, str]]] = {}
        for cell in self.cells:
            out.setdefault(cell.turma_codigo, {})[(cell.dia, cell.tempo)] = (
                cell.disciplina,
                cell.professor,
            )
        return out

    def has_critical_warnings(self) -> bool:
        return any(w.severity == "critical" for w in self.warnings)

    def mark_pending_review(self) -> None:
        self.status = IngestSnapshotStatus.pending_review

    def approve(self) -> None:
        if self.has_critical_warnings():
            raise ValueError("snapshot com avisos críticos não pode ser aprovado")
        self.status = IngestSnapshotStatus.approved

    def reject(self) -> None:
        self.status = IngestSnapshotStatus.rejected

    @classmethod
    def from_legacy_grades(
        cls,
        grades: dict[str, dict[tuple[int, int], tuple[str, str]]],
        *,
        metadata: dict[str, Any] | None = None,
    ) -> GradeSnapshot:
        cells = [
            GradeCell(
                turma_codigo=turma,
                dia=dia,
                tempo=tempo,
                disciplina=disc,
                professor=prof,
            )
            for turma, slots in grades.items()
            for (dia, tempo), (disc, prof) in slots.items()
        ]
        return cls(
            cells=cells,
            source_format=IngestSourceFormat.legacy_py,
            metadata=metadata or {"origin": "legacy_grades_dict"},
        )
