"""Auditoria independente do xlsx gravado (ADR-010)."""

from __future__ import annotations

import io
import re
import shutil
from contextlib import redirect_stdout
from pathlib import Path

from solver.legacy_bridge import legacy_context, load_verifier
from solver.models import VerifyResult

PROPOSTA_3 = 3
XLSX_PATTERN = re.compile(
    r"Proposta_3_Calendario_Provas_2026_2SEM\.xlsx",
    re.IGNORECASE,
)


def _parse_verifier_output(text: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    problemas: list[str] = []
    avisos: list[str] = []
    mode: str | None = None

    for line in text.splitlines():
        if "PROBLEMA(S)" in line:
            mode = "problema"
            continue
        if "AVISO(S)" in line:
            mode = "aviso"
            continue
        if line.startswith("OK:"):
            mode = None
            continue
        if mode == "problema" and line.startswith("  - "):
            problemas.append(line[4:].strip())
        elif mode == "aviso" and line.startswith("  ~ "):
            avisos.append(line[4:].strip())

    return tuple(problemas), tuple(avisos)


def _ensure_legacy_xlsx_name(xlsx_path: Path, work_dir: Path) -> Path:
    """O verificador legado espera nome fixo dentro de OUT."""
    expected = work_dir / f"Proposta_{PROPOSTA_3}_Calendario_Provas_2026_2SEM.xlsx"
    xlsx_path = xlsx_path.resolve()
    if xlsx_path == expected.resolve():
        return xlsx_path
    if expected.exists():
        expected.unlink()
    shutil.copy2(xlsx_path, expected)
    return expected


def verify_xlsx(
    xlsx_path: Path,
    *,
    grades: dict | None = None,
    repo_root: Path | None = None,
    work_dir: Path | None = None,
) -> VerifyResult:
    """Executa verificar_calendario.py contra o arquivo já gravado.

    PROBLEMA bloqueia entrega; AVISO é informativo (ADR-010).
    """
    xlsx_path = Path(xlsx_path)
    if not xlsx_path.is_file():
        raise FileNotFoundError(f"xlsx não encontrado: {xlsx_path}")

    out_dir = work_dir or xlsx_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    _ensure_legacy_xlsx_name(xlsx_path, out_dir)

    load_verifier(repo_root)

    buf = io.StringIO()
    with legacy_context(
        repo_root=repo_root,
        grades=grades,
        output_dir=out_dir,
    ):
        import verificar_calendario as verifier

        with redirect_stdout(buf):
            verifier.main()

    raw = buf.getvalue()
    problemas, avisos = _parse_verifier_output(raw)

    return VerifyResult(
        xlsx_path=xlsx_path,
        problemas=problemas,
        avisos=avisos,
        raw_output=raw,
    )
