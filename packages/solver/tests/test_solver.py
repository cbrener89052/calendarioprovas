"""Testes do pacote solver."""

from __future__ import annotations

from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_import_solver():
    import solver

    assert solver.__version__ == "0.2.0"
    assert callable(solver.generate_proposta3)
    assert callable(solver.verify_xlsx)


def test_legacy_bridge_finds_repo():
    from solver.legacy_bridge import find_repo_root, load_generator

    root = find_repo_root(REPO_ROOT / "packages" / "solver")
    assert (root / "gerar_calendario.py").is_file()

    g = load_generator(root)
    assert hasattr(g, "montar_proposta")
    assert len(g.GRADES) == 8


def test_grade_snapshot_from_legacy():
    from ingest.models import GradeSnapshot
    from solver.legacy_bridge import load_generator

    g = load_generator(REPO_ROOT)
    snap = GradeSnapshot.from_legacy_grades(g.GRADES)
    grades = snap.to_grades_dict()
    assert set(grades.keys()) == set(g.GRADES.keys())
    assert grades["9C1"][(1, 1)] == g.GRADES["9C1"][(1, 1)]


def test_verify_parse_output():
    from solver.verify import _parse_verifier_output

    text = (
        "2 PROBLEMA(S):\n"
        "  - P3/9C1: semana 5 com 4 avaliações\n"
        "  - P3/10C1: Mat tem 3 provas\n"
        "\n"
        "1 AVISO(S) — regras relaxadas:\n"
        "  ~ P3/10C1: regra 4 relaxada\n"
    )
    problemas, avisos = _parse_verifier_output(text)
    assert len(problemas) == 2
    assert len(avisos) == 1


@pytest.mark.slow
def test_generate_and_verify_legacy_smoke(tmp_path: Path):
    """Gera Proposta 3 com grades hardcoded e audita o xlsx (paridade CLI).

    Opt-in: export RUN_SLOW=1 (backtracking leva vários minutos).
    """
    import os

    if os.environ.get("RUN_SLOW") != "1":
        pytest.skip("defina RUN_SLOW=1 para executar geração completa")

    from solver import generate_proposta3_legacy, verify_xlsx

    modelo = REPO_ROOT / "Klausurplan_2026_2SEM.xlsx"
    if not modelo.is_file():
        pytest.skip("modelo xlsx ausente no repositório")

    out = tmp_path / "out"
    result = generate_proposta3_legacy(
        modelo_xlsx=modelo,
        output_dir=out,
        repo_root=REPO_ROOT,
    )
    assert result.xlsx_path.is_file()
    assert result.relatorio_path.is_file()

    verification = verify_xlsx(result.xlsx_path, repo_root=REPO_ROOT, work_dir=out)
    assert verification.xlsx_path == result.xlsx_path
