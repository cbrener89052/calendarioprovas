# Plano de Reconstrução — calendarioprovas

**Fonte:** migração  
**Gerado:** 2026-08-10  
**Projeto:** calendarioprovas  
**Stack:** FastAPI + PostgreSQL + React Vite + packages/solver  
**Estratégia:** Strangler Fig + Parallel Run  

> Plano bottom-up derivado de `_reversa_sdd/migration/handoff.md`. Execute uma tarefa por sessão via `/reversa-reconstructor`.

## Status

| Concluídas | Pendentes | Total |
|------------|-----------|-------|
| 1 | 13 | 14 |

---

## Tarefa 1 — Scaffold monorepo e infra

- **Status:** done
- **Lê:** `migration/topology_decision.md`, `migration/target_architecture.md`, `migration/migration_brief.md`
- **Entrega:** Estrutura `apps/api`, `apps/worker`, `apps/web`, `packages/solver`, `infra/docker-compose.yml`, `legacy/` symlink/copy
- **Critério:** `docker compose config` válido
- **Concluída:** 2026-08-10 — branch `cursor/reversa-reconstruct-b8d6`

## Tarefa 2 — Schema PostgreSQL + migrations

- **Status:** pending
- **Lê:** `migration/target_data_model.md`, `erd-complete.md`
- **Entrega:** Alembic/Flyway migrations; tabelas instituicao→relatorio
- **Critério:** migrate up/down OK

## Tarefa 3 — Seed catálogo regras

- **Status:** pending
- **Lê:** `migration/data_migration_plan.md`, `regras-negocio/requirements.md`, `.claude/skills/calendario-provas/SKILL.md` (seções regras)
- **Entrega:** `scripts/seed_catalogo_regras.py`
- **Critério:** ≥30 regras em regra_catalogo

## Tarefa 4 — Extrair packages/solver

- **Status:** pending
- **Lê:** `migration/paradigm_decision.md`, `gerar_calendario.py`, `verificar_calendario.py`
- **Entrega:** Refactor solver importável; constantes parametrizáveis via RuleContext stub
- **Critério:** pytest import solver; CLI legado ainda funciona em `legacy/`

## Tarefa 5 — Worker pipeline

- **Status:** pending
- **Lê:** `migration/target_domain_model.md`, `geracao-calendario/design.md`, `verificacao-calendario/design.md`
- **Entrega:** Job consumer: carregar blobs → solver → verificador → persistir
- **Critério:** job manual com entradas locais completa

## Tarefa 6 — API auth + tenant

- **Status:** pending
- **Lê:** `permissions.md`, `openapi/calendarioprovas.yaml`, `migration/target_architecture.md`
- **Entrega:** JWT login, segmento/me, RLS ou filtro segmento_id
- **Critério:** parity test 03 isolamento passa (manual)

## Tarefa 7 — API CRUD GRUPOS + semestres

- **Status:** pending
- **Lê:** `plataforma-multi-coordenador/design.md`, `migration/target_screens.md` SCR-03/04
- **Entrega:** Endpoints CRUD + upload blob
- **Critério:** upload grade + modelo OK

## Tarefa 8 — API regras + RuleContext

- **Status:** pending
- **Lê:** `regras-negocio/design.md`, `migration/target_business_rules.md` BR-MIGRAR-015
- **Entrega:** toggles PATCH; RuleContextBuilder
- **Critério:** parity test 04 toggles

## Tarefa 9 — API jobs + calendários

- **Status:** pending
- **Lê:** `plataforma-multi-coordenador/contracts.md`, `migration/parity_tests/01-geracao-proposta3.feature`
- **Entrega:** POST gerar, GET jobs, GET calendarios download
- **Critério:** job async end-to-end

## Tarefa 10 — Exportadores + relatórios

- **Status:** pending
- **Lê:** `exportacao-relatorios/requirements.md`, `migration/parity_tests/05-export-relatorios.feature`
- **Entrega:** blobs trocas, cessoes, tabela
- **Critério:** paridade com CLI exportadores

## Tarefa 11 — Frontend scaffold + auth

- **Status:** pending
- **Lê:** `migration/target_screens.md` SCR-01/02, `migration/screen_modernization_decision.md`
- **Entrega:** Vite React TS Tailwind; login + dashboard
- **Critério:** login JWT funcional

## Tarefa 12 — Frontend GRUPOS + uploads + regras

- **Status:** pending
- **Lê:** `migration/target_screens.md` SCR-03/04/05/06
- **Entrega:** Telas CRUD + toggles + IA
- **Critério:** fluxo config semestre completo UI

## Tarefa 13 — Frontend gerar + verificação

- **Status:** pending
- **Lê:** `migration/target_screens.md` SCR-07/08, `user-stories/fluxo-calendario-semestre.md`
- **Entrega:** Job polling, downloads, publish gate
- **Critério:** E2E feliz path

## Tarefa 14 — Parallel Run + testes paridade

- **Status:** pending
- **Lê:** `migration/cutover_plan.md`, `migration/parity_specs.md`, `migration/parity_tests/*.feature`
- **Entrega:** pytest diff xlsx; tradução Gherkin; documentação cutover
- **Critério:** 0 divergências críticas piloto

---

## Lacunas conhecidas (não bloqueiam T1)

- AMB-C01 Context vs Redux — decidir em T11
- AMB-C02 ARGB validation — T5/T10
- AMB-C03 Audit log — T8 Should
