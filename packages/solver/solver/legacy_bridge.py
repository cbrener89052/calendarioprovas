"""Carrega módulos legado da raiz do repositório sem alterá-los."""

from __future__ import annotations

import importlib
import sys
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import Iterator


def find_repo_root(start: Path | None = None) -> Path:
    """Sobe diretórios até achar gerar_calendario.py."""
    cur = (start or Path(__file__)).resolve()
    if cur.is_file():
        cur = cur.parent
    for parent in [cur, *cur.parents]:
        if (parent / "gerar_calendario.py").is_file():
            return parent
    raise FileNotFoundError(
        "gerar_calendario.py não encontrado — execute a partir do repositório calendarioprovas"
    )


def _ensure_repo_on_path(repo_root: Path) -> None:
    root = str(repo_root)
    if root not in sys.path:
        sys.path.insert(0, root)


def load_generator(repo_root: Path | None = None) -> ModuleType:
    root = repo_root or find_repo_root()
    _ensure_repo_on_path(root)
    return importlib.import_module("gerar_calendario")


def load_verifier(repo_root: Path | None = None) -> ModuleType:
    root = repo_root or find_repo_root()
    _ensure_repo_on_path(root)
    # Garante que gerar_calendario está carregado antes do verificador.
    load_generator(root)
    return importlib.import_module("verificar_calendario")


@contextmanager
def legacy_context(
    *,
    repo_root: Path | None = None,
    grades: dict | None = None,
    modelo_xlsx: Path | None = None,
    output_dir: Path | None = None,
) -> Iterator[ModuleType]:
    """Patch temporário de GRADES/SRC/OUT no módulo legado."""
    g = load_generator(repo_root)
    backup = {
        "GRADES": g.GRADES,
        "SRC": getattr(g, "SRC", None),
        "OUT": getattr(g, "OUT", None),
    }
    try:
        if grades is not None:
            g.GRADES = grades
        if modelo_xlsx is not None:
            g.SRC = str(modelo_xlsx)
        if output_dir is not None:
            g.OUT = str(output_dir)
        yield g
    finally:
        g.GRADES = backup["GRADES"]
        if backup["SRC"] is not None:
            g.SRC = backup["SRC"]
        if backup["OUT"] is not None:
            g.OUT = backup["OUT"]
