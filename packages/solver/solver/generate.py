"""Geração Proposta 3 via wrapper do legado (ADR-008)."""

from __future__ import annotations

from pathlib import Path

from ingest.models import GradeSnapshot

from solver.legacy_bridge import legacy_context, load_generator
from solver.models import GenerateResult, RelaxationState

PROPOSTA_3 = 3
DEFAULT_SEED = 3
XLSX_NAME = f"Proposta_{PROPOSTA_3}_Calendario_Provas_2026_2SEM.xlsx"


def _run_relaxation_ladder(g, seed: int) -> tuple[dict, set[str], RelaxationState]:
    """Replica a escada de afrouxamento de gerar_calendario.main()."""
    sem_r3: set[str] = set()
    sem_r4: set[str] = set()
    folga_extra: dict[str, int] = {}
    aloc3 = None

    for _etapa in range(0, 12):
        aloc, falharam = g.montar_proposta(
            seed,
            folga=0,
            sem_regra3=sem_r3,
            sem_regra4=sem_r4,
            folga_extra=folga_extra,
        )
        if aloc3 is None:
            aloc3 = aloc
        if not falharam:
            aloc3 = aloc
            break
        aloc3 = aloc
        if not sem_r4 >= falharam:
            sem_r4 |= falharam
        elif not sem_r3 >= falharam:
            sem_r3 |= falharam
        elif any(folga_extra.get(t, 0) < 3 for t in falharam):
            for t in falharam:
                folga_extra[t] = folga_extra.get(t, 0) + 1
        else:
            break

    assert aloc3 is not None
    relaxation = RelaxationState(
        sem_regra3=frozenset(sem_r3),
        sem_regra4=frozenset(sem_r4),
        folga_extra=dict(folga_extra),
    )
    return aloc3, falharam, relaxation


def generate_proposta3(
    snapshot: GradeSnapshot,
    *,
    modelo_xlsx: Path,
    output_dir: Path,
    seed: int = DEFAULT_SEED,
    repo_root: Path | None = None,
) -> GenerateResult:
    """Gera Proposta 3 a partir de GradeSnapshot aprovado.

    O solver nunca re-parseia PDF — só consome células já normalizadas (ADR-008).
    """
    if snapshot.status.value != "approved":
        raise ValueError(
            f"snapshot deve estar approved, recebido: {snapshot.status.value}"
        )

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    modelo_xlsx = Path(modelo_xlsx)
    if not modelo_xlsx.is_file():
        raise FileNotFoundError(f"modelo xlsx não encontrado: {modelo_xlsx}")

    grades = snapshot.to_grades_dict()

    with legacy_context(
        repo_root=repo_root,
        grades=grades,
        modelo_xlsx=modelo_xlsx,
        output_dir=output_dir,
    ) as g:
        g.carregar_ocupadas()
        comuns_por_par = {
            (a, b): g.classificar_par(a, b) for a, b in g.PARES_IRMAS
        }

        aloc, falharam, relaxation = _run_relaxation_ladder(g, seed)
        xlsx_path = Path(g.escrever(PROPOSTA_3, aloc))
        relatorio_path = Path(
            g.relatorio({PROPOSTA_3: aloc}, comuns_por_par)
        )

    return GenerateResult(
        xlsx_path=xlsx_path,
        relatorio_path=relatorio_path,
        alocacoes=aloc,
        falharam=frozenset(falharam),
        relaxation=relaxation,
        seed=seed,
        proposta=PROPOSTA_3,
    )


def generate_proposta3_legacy(
    *,
    modelo_xlsx: Path | None = None,
    output_dir: Path | None = None,
    seed: int = DEFAULT_SEED,
    repo_root: Path | None = None,
) -> GenerateResult:
    """Gera usando GRADES hardcoded do legado (paridade CLI)."""
    g = load_generator(repo_root)
    root = repo_root or Path(g.BASE)
    out = output_dir or Path(g.OUT)
    modelo = modelo_xlsx or Path(g.SRC)

    from ingest.models import GradeSnapshot

    snapshot = GradeSnapshot.from_legacy_grades(
        g.GRADES,
        metadata={"origin": "legacy_hardcoded"},
    )
    snapshot.approve()

    return generate_proposta3(
        snapshot,
        modelo_xlsx=modelo,
        output_dir=out,
        seed=seed,
        repo_root=root,
    )


def expected_xlsx_name() -> str:
    return XLSX_NAME
