"""Validação pós-extração e geração de avisos para check-in."""

from __future__ import annotations

from collections import defaultdict

from ingest.models import GradeCell, GradeSnapshot, IngestSnapshotStatus, IngestWarning

EXPECTED_TEMPOS = 11
EXPECTED_DIAS = 5


def validate_snapshot(snapshot: GradeSnapshot) -> GradeSnapshot:
    warnings = list(snapshot.warnings)
    by_turma: dict[str, list[GradeCell]] = defaultdict(list)
    for cell in snapshot.cells:
        by_turma[cell.turma_codigo].append(cell)

    if not snapshot.cells:
        warnings.append(
            IngestWarning(
                code="EMPTY_SNAPSHOT",
                message="nenhuma célula extraída",
                severity="critical",
            )
        )

    seen: set[tuple[str, int, int]] = set()
    for cell in snapshot.cells:
        key = (cell.turma_codigo, cell.dia, cell.tempo)
        if key in seen:
            warnings.append(
                IngestWarning(
                    code="DUPLICATE_SLOT",
                    message=f"slot duplicado ({cell.dia}, {cell.tempo})",
                    turma_codigo=cell.turma_codigo,
                    dia=cell.dia,
                    tempo=cell.tempo,
                    severity="critical",
                )
            )
        seen.add(key)

        if not cell.disciplina:
            warnings.append(
                IngestWarning(
                    code="EMPTY_DISCIPLINA",
                    message="disciplina vazia",
                    turma_codigo=cell.turma_codigo,
                    dia=cell.dia,
                    tempo=cell.tempo,
                    severity="critical",
                )
            )

    for turma, cells in sorted(by_turma.items()):
        slots = {(c.dia, c.tempo) for c in cells}
        if len(slots) < 10:
            warnings.append(
                IngestWarning(
                    code="SPARSE_GRADE",
                    message=f"turma {turma} com apenas {len(slots)} células preenchidas",
                    turma_codigo=turma,
                    severity="warning",
                )
            )

    status = snapshot.status
    if any(w.severity == "critical" for w in warnings):
        status = IngestSnapshotStatus.pending_review
    elif status == IngestSnapshotStatus.draft:
        status = IngestSnapshotStatus.pending_review

    return GradeSnapshot(
        cells=snapshot.cells,
        source_format=snapshot.source_format,
        status=status,
        warnings=warnings,
        snapshot_id=snapshot.snapshot_id,
        semestre_id=snapshot.semestre_id,
        metadata=snapshot.metadata,
    )
