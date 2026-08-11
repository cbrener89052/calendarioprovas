# Plano de Reconstrução — calendarioprovas

**Fonte:** migração  
**Gerado:** 2026-08-10  
**Projeto:** calendarioprovas  
**Stack:** FastAPI + PostgreSQL + React Vite + packages/solver + packages/ingest  
**Estratégia:** Strangler Fig + Parallel Run  

> Plano bottom-up derivado de `_reversa_sdd/migration/handoff.md`. Execute uma tarefa por sessão via `/reversa-reconstructor`.

## Status

| Concluídas | Pendentes | Total |
|------------|-----------|-------|
| 6 | 12 | 18 |

---

## Tarefa 1 — Scaffold monorepo e infra

- **Status:** done
- **Lê:** `migration/topology_decision.md`, `migration/target_architecture.md`, `migration/migration_brief.md`
- **Entrega:** Estrutura `apps/api`, `apps/worker`, `apps/web`, `packages/solver`, `infra/docker-compose.yml`, `legacy/` symlink/copy
- **Critério:** `docker compose config` válido
- **Concluída:** 2026-08-10 — branch `cursor/reversa-reconstruct-b8d6`

## Tarefa 2 — Schema PostgreSQL + migrations

- **Status:** done
- **Lê:** `migration/target_data_model.md`, `erd-complete.md`
- **Entrega:** Alembic/Flyway migrations; tabelas instituicao→relatorio
- **Critério:** migrate up/down OK
- **Concluída:** 2026-08-10 — schema `calendario`, 13 tabelas, revision `48f843bb6ab4`

## Tarefa 3 — Seed catálogo regras

- **Status:** done
- **Lê:** `migration/data_migration_plan.md`, `regras-negocio/requirements.md`, `.claude/skills/calendario-provas/SKILL.md` (seções regras)
- **Entrega:** `scripts/seed_catalogo_regras.py`
- **Critério:** ≥30 regras em regra_catalogo
- **Concluída:** 2026-08-10 — 38 regras seed (idempotente)

## Tarefa 3b — Schema ingestão (grade_celula + ingest_snapshot)

- **Status:** done
- **Lê:** `adrs/008-ingestao-snapshot-aprovado.md`, `erd-complete.md`
- **Entrega:** Migration Alembic `a1b2c3d4e5f6`; models SQLAlchemy; enums status/formato
- **Critério:** migrate up/down OK; FK semestre→snapshot→celula
- **Concluída:** 2026-08-10 — ADR-008 + revision `a1b2c3d4e5f6`

## Tarefa 3c — Pacote packages/ingest

- **Status:** done
- **Lê:** `extracao-grade/design.md`, `extrair_grade_2025.py`, ADR-008
- **Entrega:** `packages/ingest` com models (`GradeSnapshot`), extract_pdf/xlsx (stub), normalize, validate
- **Critério:** importável; contrato `to_grades_dict()` compatível com legado
- **Concluída:** 2026-08-10 — esqueleto T3c

## Tarefa 3d — CLI check-in revisor

- **Status:** done
- **Lê:** ADR-008, `extracao-grade/requirements.md` (RN-03 avisos)
- **Entrega:** `python -m ingest.checkin` (--legacy-py, --snapshot, --approve)
- **Critério:** bloqueia aprovação com avisos críticos; imprime relatório
- **Concluída:** 2026-08-10 — CLI T3d

## Tarefa 4 — API upload grade + persist snapshot

- **Status:** pending
- **Lê:** `extracao-grade/design.md`, `plataforma-multi-coordenador/contracts.md`
- **Entrega:** POST upload → job extração → snapshot `pending_review`; GET preview avisos
- **Critério:** upload PDF persiste ingest_snapshot + grade_celula

## Tarefa 5 — Extrair packages/solver

- **Status:** pending
- **Lê:** `migration/paradigm_decision.md`, `gerar_calendario.py`, `verificar_calendario.py`, ADR-008
- **Entrega:** Refactor solver importável; lê `GradeSnapshot` aprovado (nunca re-parse PDF)
- **Critério:** pytest import solver; CLI legado ainda funciona em `legacy/`

## Tarefa 6 — Worker pipeline

- **Status:** pending
- **Lê:** `migration/target_domain_model.md`, `geracao-calendario/design.md`, `verificacao-calendario/design.md`
- **Entrega:** Job consumer: carregar snapshot aprovado → solver → verificador → persistir
- **Critério:** job manual com entradas locais completa

## Tarefa 7 — API auth + tenant

- **Status:** pending
- **Lê:** `permissions.md`, `openapi/calendarioprovas.yaml`, `migration/target_architecture.md`
- **Entrega:** JWT login, segmento/me, RLS ou filtro segmento_id
- **Critério:** parity test 03 isolamento passa (manual)

## Tarefa 8 — API CRUD GRUPOS + semestres

- **Status:** pending
- **Lê:** `plataforma-multi-coordenador/design.md`, `migration/target_screens.md` SCR-03/04
- **Entrega:** Endpoints CRUD + upload blob
- **Critério:** upload grade + modelo OK

## Tarefa 9 — API regras + RuleContext

- **Status:** pending
- **Lê:** `regras-negocio/design.md`, `migration/target_business_rules.md` BR-MIGRAR-015
- **Entrega:** toggles PATCH; RuleContextBuilder
- **Critério:** parity test 04 toggles

## Tarefa 10 — API jobs + calendários

- **Status:** pending
- **Lê:** `plataforma-multi-coordenador/contracts.md`, `migration/parity_tests/01-geracao-proposta3.feature`
- **Entrega:** POST gerar, GET jobs, GET calendarios download
- **Critério:** job async end-to-end

## Tarefa 11 — Exportadores + relatórios

- **Status:** pending
- **Lê:** `exportacao-relatorios/requirements.md`, `migration/parity_tests/05-export-relatorios.feature`, ADR-009
- **Entrega:** blobs trocas, cessoes, tabela; INSERT-only nova versão `calendario_gerado` por job
- **Critério:** paridade com CLI exportadores; histórico acumula versões

## Tarefa 11b — API histórico calendários

- **Status:** pending
- **Lê:** ADR-009, `plataforma-multi-coordenador/contracts.md`
- **Entrega:** GET `/semestres/{id}/calendarios`, DELETE, POST restaurar-referencia; migration colunas versao/deleted_at
- **Critério:** coordenador lista e apaga versão via API

## Tarefa 12 — Frontend scaffold + auth

- **Status:** pending
- **Lê:** `migration/target_screens.md` SCR-01/02, `migration/screen_modernization_decision.md`
- **Entrega:** Vite React TS Tailwind; login + dashboard
- **Critério:** login JWT funcional

## Tarefa 13 — Frontend GRUPOS + uploads + regras + check-in grade

- **Status:** pending
- **Lê:** `migration/target_screens.md` SCR-03/04/05/06, ADR-008
- **Entrega:** Telas CRUD + toggles + IA + revisor avisos OCR
- **Critério:** fluxo config semestre + aprovar snapshot completo UI

## Tarefa 13b — Frontend histórico calendários (SCR-10)

- **Status:** pending
- **Lê:** ADR-009, SCR-10, RF-15–RF-18
- **Entrega:** Lista versões, download, apagar, restaurar referência
- **Critério:** pós-geração nova versão visível sem ação manual

## Tarefa 14 — Frontend gerar + verificação

- **Status:** pending
- **Lê:** `migration/target_screens.md` SCR-07/08, `user-stories/fluxo-calendario-semestre.md`
- **Entrega:** Job polling, downloads, publish gate
- **Critério:** E2E feliz path

## Tarefa 15 — Parallel Run + testes paridade

- **Status:** pending
- **Lê:** `migration/cutover_plan.md`, `migration/parity_specs.md`, `migration/parity_tests/*.feature`
- **Entrega:** pytest diff xlsx; tradução Gherkin; documentação cutover
- **Critério:** 0 divergências críticas piloto

---

## Lacunas conhecidas (não bloqueiam T1)

- AMB-C01 Context vs Redux — decidir em T12
- AMB-C02 ARGB validation — T6/T11
- AMB-C03 Audit log — T9 Should
- extract_pdf/xlsx completos — migrar lógica legado em T4/T5
