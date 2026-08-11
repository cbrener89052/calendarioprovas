#!/usr/bin/env python3
"""Seed mínimo para testar T4 upload/ingest (dev local)."""

from __future__ import annotations

import os
import sys
import uuid
from datetime import date
from pathlib import Path

API_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(API_DIR))

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://calendario:calendario@localhost:5432/calendario",
)

from sqlalchemy import select  # noqa: E402

from app.db.enums import PapelCoordenador  # noqa: E402
from app.db.models import Coordenador, Grupo, Instituicao, Segmento, Semestre, Turma  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402

TURMAS = ["9C1", "9C2", "10C1", "10C2", "11C1", "11C2", "12C1", "12C2"]


def main() -> None:
    db = SessionLocal()
    try:
        inst = db.scalar(select(Instituicao).where(Instituicao.nome == "Escola Alemã Corcovado (dev)"))
        if inst is None:
            inst = Instituicao(nome="Escola Alemã Corcovado (dev)")
            db.add(inst)
            db.flush()

        coord = db.scalar(select(Coordenador).where(Coordenador.email == "dev@escola.local"))
        if coord is None:
            coord = Coordenador(
                instituicao_id=inst.id,
                email="dev@escola.local",
                nome="Coordenador Dev",
                papel=PapelCoordenador.coordenador,
                senha_hash="dev",
            )
            db.add(coord)
            db.flush()

        seg = db.scalar(select(Segmento).where(Segmento.coordenador_id == coord.id))
        if seg is None:
            seg = Segmento(coordenador_id=coord.id, nome="Ensino Médio C (dev)")
            db.add(seg)
            db.flush()

        grupo = db.scalar(
            select(Grupo).where(Grupo.segmento_id == seg.id, Grupo.nome == "10/12 dev")
        )
        if grupo is None:
            grupo = Grupo(
                segmento_id=seg.id,
                nome="10/12 dev",
                data_inicio_semestre=date(2026, 8, 4),
                data_fim_semestre=date(2026, 11, 28),
                datas_segunda_chamada=["2026-11-10"],
                conselho_inicio=date(2026, 11, 24),
                conselho_fim=date(2026, 11, 28),
            )
            db.add(grupo)
            db.flush()

        for codigo in TURMAS:
            if db.scalar(select(Turma).where(Turma.codigo == codigo)) is None:
                db.add(Turma(grupo_id=grupo.id, codigo=codigo))

        sem = db.scalar(
            select(Semestre).where(
                Semestre.segmento_id == seg.id, Semestre.ano == 2026, Semestre.periodo == 2
            )
        )
        if sem is None:
            sem = Semestre(
                segmento_id=seg.id,
                ano=2026,
                periodo=2,
                inicio=date(2026, 8, 4),
                fim=date(2026, 11, 28),
            )
            db.add(sem)
            db.flush()

        db.commit()
        print(f"semestre_id={sem.id}")
        print(f"segmento_id={seg.id}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
