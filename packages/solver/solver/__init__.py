"""Calendário de provas — solver Proposta 3 (wrapper legado, T5)."""

from solver.generate import (
    DEFAULT_SEED,
    generate_proposta3,
    generate_proposta3_legacy,
)
from solver.models import GenerateResult, RelaxationState, VerifyResult
from solver.verify import verify_xlsx

__version__ = "0.2.0"

__all__ = [
    "DEFAULT_SEED",
    "GenerateResult",
    "RelaxationState",
    "VerifyResult",
    "generate_proposta3",
    "generate_proposta3_legacy",
    "verify_xlsx",
]
