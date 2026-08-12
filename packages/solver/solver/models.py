"""Tipos de resultado do solver (geração e verificação)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RelaxationState:
    """Estado de afrouxamento da escada da Proposta 3."""

    sem_regra3: frozenset[str] = frozenset()
    sem_regra4: frozenset[str] = frozenset()
    folga_extra: dict[str, int] = field(default_factory=dict)

    @property
    def had_relaxation(self) -> bool:
        return bool(self.sem_regra3 or self.sem_regra4 or self.folga_extra)


@dataclass(frozen=True)
class GenerateResult:
    """Saída da geração Proposta 3."""

    xlsx_path: Path
    relatorio_path: Path
    alocacoes: dict[str, list[Any]]
    falharam: frozenset[str]
    relaxation: RelaxationState
    seed: int
    proposta: int = 3

    @property
    def ok(self) -> bool:
        return not self.falharam


@dataclass(frozen=True)
class VerifyResult:
    """Saída da auditoria independente do xlsx (ADR-010)."""

    xlsx_path: Path
    problemas: tuple[str, ...]
    avisos: tuple[str, ...]
    raw_output: str = ""

    @property
    def ok(self) -> bool:
        return not self.problemas

    @property
    def blocked(self) -> bool:
        """PROBLEMA impede entrega; AVISO não."""
        return bool(self.problemas)
