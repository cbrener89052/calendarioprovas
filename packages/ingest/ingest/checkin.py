#!/usr/bin/env python3
"""CLI revisor de check-in da grade (T3d).

Uso:
    python -m ingest.checkin --snapshot snapshot.json
    python -m ingest.checkin --legacy-py horarios2025/grade_2sem_2025.py
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Any

from ingest.models import GradeSnapshot, IngestSnapshotStatus
from ingest.normalize import normalize_snapshot
from ingest.validate import validate_snapshot


def _parse_cell_value(value: Any) -> tuple[str, str]:
    if isinstance(value, (list, tuple)) and value and isinstance(value[0], (list, tuple)):
        pairs = [(str(d), str(p)) for d, p in value]
        disc = pairs[0][0]
        prof = "-".join(p[1] for p in pairs)
        return disc, prof
    if isinstance(value, (list, tuple)) and len(value) == 2:
        return str(value[0]), str(value[1])
    if isinstance(value, str):
        if "/" in value:
            disc, prof = value.split("/", 1)
            return disc.strip(), prof.strip()
        parts = value.split()
        if len(parts) >= 2:
            return parts[0], parts[1]
    raise ValueError(f"valor de célula inválido: {value!r}")


def load_legacy_py(path: Path) -> GradeSnapshot:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    grades = None
    grade_names = ("GRADES", "GRADE_TXT", "GRADE_2025", "GRADE_1SEM", "GRADE")
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in grade_names:
                    grades = ast.literal_eval(node.value)
                    break
    if grades is None:
        raise ValueError(f"nenhum dict GRADES/GRADE_* encontrado em {path}")

    converted: dict[str, dict[tuple[int, int], tuple[str, str]]] = {}
    for turma, slots in grades.items():
        converted[turma] = {}
        for key, value in slots.items():
            if isinstance(key, (list, tuple)) and len(key) == 2:
                dia, tempo = int(key[0]), int(key[1])
            else:
                raise ValueError(f"chave de slot inválida: {key!r}")
            disc, prof = _parse_cell_value(value)
            converted[turma][(dia, tempo)] = (disc, prof)

    return GradeSnapshot.from_legacy_grades(converted, metadata={"source_file": str(path)})


def load_snapshot_json(path: Path) -> GradeSnapshot:
    data = json.loads(path.read_text(encoding="utf-8"))
    from ingest.models import GradeCell, IngestSourceFormat, IngestWarning, IngestSnapshotStatus

    cells = [GradeCell(**c) for c in data.get("cells", [])]
    warnings = [IngestWarning(**w) for w in data.get("warnings", [])]
    return GradeSnapshot(
        cells=cells,
        source_format=IngestSourceFormat(data["source_format"]),
        status=IngestSnapshotStatus(data.get("status", "draft")),
        warnings=warnings,
        snapshot_id=data.get("snapshot_id"),
        semestre_id=data.get("semestre_id"),
        metadata=data.get("metadata", {}),
    )


def print_report(snapshot: GradeSnapshot) -> int:
    turmas = sorted({c.turma_codigo for c in snapshot.cells})
    print(f"Status: {snapshot.status.value}")
    print(f"Checksum: {snapshot.checksum()}")
    print(f"Turmas: {len(turmas)} ({', '.join(turmas) if turmas else '—'})")
    print(f"Células: {len(snapshot.cells)}")
    print(f"Avisos: {len(snapshot.warnings)}")

    critical = [w for w in snapshot.warnings if w.severity == "critical"]
    warnings = [w for w in snapshot.warnings if w.severity == "warning"]
    if critical:
        print("\n--- Críticos ---")
        for w in critical:
            loc = f" {w.turma_codigo} ({w.dia},{w.tempo})" if w.turma_codigo else ""
            print(f"  [{w.code}]{loc}: {w.message}")
    if warnings:
        print("\n--- Avisos ---")
        for w in warnings[:20]:
            loc = f" {w.turma_codigo} ({w.dia},{w.tempo})" if w.turma_codigo else ""
            print(f"  [{w.code}]{loc}: {w.message}")
        if len(warnings) > 20:
            print(f"  ... +{len(warnings) - 20} avisos")

    if snapshot.has_critical_warnings():
        print("\n❌ Check-in bloqueado: corrija avisos críticos antes de aprovar.")
        return 1
    print("\n✅ Check-in OK: snapshot pode ser aprovado.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Revisor de check-in da grade (ADR-008)")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--snapshot", type=Path, help="JSON GradeSnapshot")
    src.add_argument("--legacy-py", type=Path, help="Arquivo .py com dict GRADES")
    parser.add_argument("--approve", action="store_true", help="marca snapshot como approved se válido")
    args = parser.parse_args(argv)

    if args.snapshot:
        snapshot = load_snapshot_json(args.snapshot)
    else:
        snapshot = load_legacy_py(args.legacy_py)

    snapshot = normalize_snapshot(snapshot)
    snapshot = validate_snapshot(snapshot)

    if args.approve and not snapshot.has_critical_warnings():
        snapshot.approve()

    return print_report(snapshot)


if __name__ == "__main__":
    sys.exit(main())
