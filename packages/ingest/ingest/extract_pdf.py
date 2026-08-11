"""Extração de grade a partir de PDF Untis."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ingest.models import GradeCell, GradeSnapshot, IngestSourceFormat, IngestWarning


def extract_pdf(path: str | Path, *, layout: dict[str, Any] | None = None) -> GradeSnapshot:
    """Extrai grade de PDF; delega geometria ao legado quando disponível.

    T3c: esqueleto — implementação completa migra lógica de extrair_grade_2025.py.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    try:
        import pymupdf  # noqa: F401
    except ImportError as exc:
        raise RuntimeError("instale pymupdf: pip install 'calendarioprovas-ingest[pdf]'") from exc

    warnings = [
        IngestWarning(
            code="NOT_IMPLEMENTED",
            message=f"extract_pdf ainda não implementado para {path.name}; use legacy_py ou xlsx",
            severity="critical",
        )
    ]
    return GradeSnapshot(
        cells=[],
        source_format=IngestSourceFormat.pdf,
        warnings=warnings,
        metadata={"path": str(path), "layout": layout or {}},
    )


def extract_pdf_page_cells(
    words: list[tuple[float, float, float, float, str]],
    turma_codigo: str,
    celula_da,
) -> tuple[list[GradeCell], list[IngestWarning]]:
    """Utilitário: palavras OCR → células (reutiliza celula_da do legado)."""
    from collections import defaultdict

    grupos: dict[tuple[int, int], list[tuple[float, float, str]]] = defaultdict(list)
    warnings: list[IngestWarning] = []

    for x, y, _w, _h, txt in words:
        slot = celula_da(x, y)
        if slot is None:
            warnings.append(
                IngestWarning(
                    code="UNMAPPED_WORD",
                    message=f"palavra '{txt}' fora da grade",
                    turma_codigo=turma_codigo,
                    severity="warning",
                )
            )
            continue
        dia, tempo = slot
        grupos[(dia, tempo)].append((y, x, txt))

    cells: list[GradeCell] = []
    for (dia, tempo), itens in sorted(grupos.items()):
        itens.sort()
        texto = " ".join(t for _y, _x, t in itens)
        if "/" not in texto:
            warnings.append(
                IngestWarning(
                    code="MISSING_SEPARATOR",
                    message=f"célula sem disciplina/professor: {texto!r}",
                    turma_codigo=turma_codigo,
                    dia=dia,
                    tempo=tempo,
                    severity="critical",
                )
            )
            continue
        disc, prof = texto.split("/", 1)
        cells.append(
            GradeCell(
                turma_codigo=turma_codigo,
                dia=dia,
                tempo=tempo,
                disciplina=disc.strip().lower(),
                professor=prof.strip(),
            )
        )
    return cells, warnings
