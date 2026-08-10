#!/usr/bin/env python3
"""Seed REGRA_CATALOGO a partir da skill calendario-provas e mapeamento solver."""

from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "apps" / "api"
sys.path.insert(0, str(API_DIR))

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://calendario:calendario@localhost:5432/calendario",
)

from sqlalchemy import select  # noqa: E402

from app.db.models import Instituicao, RegraCatalogo  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402

SKILL = ".claude/skills/calendario-provas/SKILL.md"

REGRAS: list[dict] = [
    {
        "codigo": "max_3_avaliacoes_semana",
        "descricao": "Máximo de 3 avaliações por semana por turma; simulado conta como 1.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#máximo-de-3-avaliações-por-semana",
    },
    {
        "codigo": "uma_prova_por_dia",
        "descricao": "Uma prova por dia por turma.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#uma-prova-por-dia",
    },
    {
        "codigo": "distancia_4_semanas_mesma_disciplina",
        "descricao": "Distância entre provas: escada tenta 7 semanas, piso rígido 4 semanas (código enforce 4).",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#distância-entre-as-2-provas",
    },
    {
        "codigo": "grupo_1_semana_unica",
        "descricao": "Grupo 1 (Mat, DaF, Port/Ing): no máximo 1 prova por semana entre essas disciplinas.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#grupo-1",
    },
    {
        "codigo": "lp_lit_red_bloco_3_tempos",
        "descricao": "Turmas 10–12: bloco LP+LIT+RED de 3 tempos consecutivos no mesmo dia.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#lp-lit-red-turmas-10-11-e-12",
    },
    {
        "codigo": "lp_lit_red_10_dias_conselho",
        "descricao": "LP/LIT/RED ≥10 dias antes conselho; limite por grupo via CC (BASE=9 + dict por grupo_turma).",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#lp-lit-red-prazo-mínimo-antes-do-conselho",
    },
    {
        "codigo": "quimica_fis_bio_9c_semanas_12_14",
        "descricao": "Química, Física e Biologia 9C (1 prova) entre semanas 12 e 14 do semestre.",
        "implementada_solver": False,
        "skill_ref": f"{SKILL}#química-física-e-biologia-das-turmas-9c",
    },
    {
        "codigo": "vespera_2ch_9c",
        "descricao": "Turmas 9C: nenhuma prova no dia anterior à 2ª chamada da série.",
        "implementada_solver": False,
        "skill_ref": f"{SKILL}#véspera-de-2ª-chamada-turmas-9c",
    },
    {
        "codigo": "cc_10_12_6_dias_minimo",
        "descricao": "Turmas 12C: provas pelo menos 6 dias antes do último conselho (CC 10,12).",
        "implementada_solver": False,
        "skill_ref": f"{SKILL}#12c-distância-mínima-do-conselho",
    },
    {
        "codigo": "semana_17_9c_11c_prova",
        "descricao": "Semana 17 das turmas 9C/11C deve ter pelo menos 1 prova.",
        "implementada_solver": False,
        "skill_ref": f"{SKILL}#semana-17-das-turmas-9c11c",
    },
    {
        "codigo": "evitar_tempos_7_a_11",
        "descricao": "Preferência forte por evitar tempos 7–11 (após 12h45).",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#evitar-os-tempos-7-a-11",
    },
    {
        "codigo": "nao_cruzar_recreio",
        "descricao": "Prova de tempos seguidos não pode cruzar o intervalo do recreio.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#nunca-cruzar-o-intervalo-do-recreio",
    },
    {
        "codigo": "turmas_irmaas_mesmo_professor",
        "descricao": "Coordenar provas simultâneas quando mesmo professor leciona turmas irmãs em horários diferentes.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#disciplina-com-professor-comum-entre-turmas-irmãs",
    },
    {
        "codigo": "grupos_paralelos_prova_simultanea",
        "descricao": "Grupos paralelos: 1 prova, professores simultâneos, conta como 1 avaliação.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#grupos-paralelos",
    },
    {
        "codigo": "simulados_fixos",
        "descricao": "Simulados/AG entram nas datas informadas; fixos, não movidos pelo solver.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#simuladosag",
    },
    {
        "codigo": "disciplina_1_prova_semestre",
        "descricao": "Disciplinas com 1 tempo semanal ou regra de série têm só 1 prova no semestre.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#disciplinas-com-1-prova-no-semestre",
    },
    {
        "codigo": "disciplinas_sem_prova",
        "descricao": "Ed.Física, Artes, eletivas, apoio etc. não recebem prova.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#confirmar-quais-disciplinas-não-têm-prova",
    },
    {
        "codigo": "periodo_por_grupo",
        "descricao": "Provas apenas dentro do período do GRUPO da turma.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#períodos-de-provas-por-turma",
    },
    {
        "codigo": "feriados_vetados",
        "descricao": "Excluir feriados nacionais e dias vetados do calendário civil.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#feriados-e-dias-vetados",
    },
    {
        "codigo": "semana_vetada_conselho",
        "descricao": "Semana vetada de conselho de classe sem provas.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#semanas-inteiras-vetadas",
    },
    {
        "codigo": "cessao_regra_1_teto_11pct",
        "descricao": "Cessão Proposta 3 regra 1: teto 11% da carga horária semestral por disciplina.",
        "implementada_solver": True,
        "skill_ref": "ADR-002-limites-cessao-proposta-3",
    },
    {
        "codigo": "cessao_regra_2_uma_aula_semana",
        "descricao": "Cessão regra 2: no máximo 1 aula cedida por semana por disciplina.",
        "implementada_solver": True,
        "skill_ref": "ADR-002-limites-cessao-proposta-3",
    },
    {
        "codigo": "cessao_regra_3_folga_2_semanas",
        "descricao": "Cessão regra 3: duas semanas sem contato com a turma após cessão.",
        "implementada_solver": True,
        "skill_ref": "ADR-002-limites-cessao-proposta-3",
    },
    {
        "codigo": "cessao_regra_4_pos_prova",
        "descricao": "Cessão regra 4: só ceder depois da própria prova (relaxável na escada).",
        "implementada_solver": True,
        "skill_ref": "ADR-003-regra-4-so-depois-da-prova",
    },
    {
        "codigo": "cessao_regra_5_vespera_prova",
        "descricao": "Cessão regra 5: proibido ceder na véspera da própria prova.",
        "implementada_solver": True,
        "skill_ref": "ADR-002-limites-cessao-proposta-3",
    },
    {
        "codigo": "folga_extra_por_turma",
        "descricao": "Folga extra de cessão localizada por turma (PR #18).",
        "implementada_solver": True,
        "skill_ref": "_reversa_sdd/addenda/sync-skill-2026-08-10.md",
    },
    {
        "codigo": "escada_afrouxamento",
        "descricao": "Escada: regra 4 → regra 3 → tetos +1; FORCAR_DATA nunca relaxa.",
        "implementada_solver": True,
        "skill_ref": "geracao-calendario/requirements.md#RF-04",
    },
    {
        "codigo": "relatorio_regras_relaxadas",
        "descricao": "Relatório de trocas deve listar regras relaxadas quando ocorrer afrouxamento.",
        "implementada_solver": True,
        "skill_ref": "gerar_calendario.py:detectar_regras_relaxadas",
    },
    {
        "codigo": "preferencia_primeiros_tempos",
        "descricao": "Preferência por alocar provas nos primeiros tempos do dia.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#tempo-de-aplicação",
    },
    {
        "codigo": "tempo_proprio_disciplina",
        "descricao": "Preferir tempo(s) da própria disciplina; emprestar de outra se necessário.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#tempos-emprestados",
    },
    {
        "codigo": "redacao_port_9_separadas",
        "descricao": "Turmas 9: Redação e Português são provas separadas de 2 tempos cada.",
        "implementada_solver": True,
        "skill_ref": f"{SKILL}#passo-0-pergunta-5",
    },
    {
        "codigo": "verificador_max_3_semana",
        "descricao": "Verificador: check máximo 3 avaliações/semana.",
        "implementada_solver": True,
        "skill_ref": "verificar_calendario.py",
    },
    {
        "codigo": "verificador_lp_lit_red_conselho",
        "descricao": "Verificador check 5a-bis: LP/LIT/RED ≥10 dias antes conselho.",
        "implementada_solver": True,
        "skill_ref": "verificar_calendario.py",
    },
    {
        "codigo": "verificador_cores_argb",
        "descricao": "Validação de cores ARGB no calendário xlsx.",
        "implementada_solver": False,
        "skill_ref": f"{SKILL}#cores-no-calendário",
    },
    {
        "codigo": "seed_proposta_3",
        "descricao": "Semente determinística SEED_PROPOSTA_3=3 para reprodutibilidade.",
        "implementada_solver": True,
        "skill_ref": "gerar_calendario.py:678",
    },
    {
        "codigo": "limite_dia_grupo",
        "descricao": "Último dia útil de provas por grupo (ex. 9_11 semana 17).",
        "implementada_solver": True,
        "skill_ref": "gerar_calendario.py:LIMITE_DIA",
    },
    {
        "codigo": "customizacao_ia_verificador",
        "descricao": "Customização IA usada no verificador + relatório auxiliar (não altera solver).",
        "implementada_solver": False,
        "skill_ref": "ADR-006-segmento-regras-configuraveis-ia",
    },
    {
        "codigo": "toggle_regra_configuravel",
        "descricao": "Regras codificadas podem ser desativadas via REGRA_CONFIG por semestre.",
        "implementada_solver": False,
        "skill_ref": "regras-negocio/requirements.md#RF-03",
    },
]


def seed_instituicao(db) -> Instituicao:
    inst = db.scalar(select(Instituicao).where(Instituicao.nome == "Escola Alemã Corcovado"))
    if inst:
        return inst
    inst = Instituicao(id=uuid.uuid4(), nome="Escola Alemã Corcovado")
    db.add(inst)
    db.flush()
    return inst


def seed_regras(db, instituicao: Instituicao) -> tuple[int, int]:
    created = updated = 0
    for item in REGRAS:
        existing = db.scalar(select(RegraCatalogo).where(RegraCatalogo.codigo == item["codigo"]))
        if existing:
            existing.descricao = item["descricao"]
            existing.implementada_solver = item["implementada_solver"]
            existing.skill_ref = item["skill_ref"]
            existing.instituicao_id = instituicao.id
            updated += 1
        else:
            db.add(
                RegraCatalogo(
                    id=uuid.uuid4(),
                    instituicao_id=instituicao.id,
                    codigo=item["codigo"],
                    descricao=item["descricao"],
                    implementada_solver=item["implementada_solver"],
                    skill_ref=item["skill_ref"],
                )
            )
            created += 1
    return created, updated


def main() -> int:
    if len(REGRAS) < 30:
        print(f"ERRO: catálogo tem apenas {len(REGRAS)} regras (mínimo 30)", file=sys.stderr)
        return 1

    with SessionLocal() as db:
        inst = seed_instituicao(db)
        created, updated = seed_regras(db, inst)
        db.commit()
        count = len(db.scalars(select(RegraCatalogo)).all())
        print(f"Instituição: {inst.nome} ({inst.id})")
        print(f"Regras: {count} total ({created} criadas, {updated} atualizadas)")
        if count < 30:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
