---
schemaVersion: 1
generatedAt: 2026-08-10T02:25:00Z
reversa:
  version: "1.2.58"
kind: handoff
producedBy: orchestrator
---

# Handoff para o Agente de Codificação

> Porta de entrada para implementar calendarioprovas na stack alvo (FastAPI + React + PostgreSQL + solver Python).

## ⚠️ Leitura obrigatória primeiro

1. **`paradigm_decision.md`** — híbrido pragmático: camadas API + solver procedural preservado.
2. **`topology_decision.md`** — modernizar: monorepo `apps/` + `packages/solver/`.
3. **`screen_modernization_decision.md`** — modernizado (legado CLI sem UI).

## Ordem de leitura recomendada

1. `paradigm_decision.md`
2. `topology_decision.md`
3. `screen_modernization_decision.md`
4. `migration_brief.md`
5. `target_business_rules.md`
6. `migration_strategy.md`
7. `target_architecture.md`
8. `target_domain_model.md`
9. `target_data_model.md`
10. `data_migration_plan.md`
11. `target_screens.md`
12. `parity_specs.md` + `parity_tests/`
13. `risk_register.md` + `cutover_plan.md`
14. `discard_log.md` (consultivo)
15. `ambiguity_log.md` (consultivo)

## Lista de artefatos produzidos

| Artefato | Produzido por | Status |
|---|---|---|
| migration_brief.md | orchestrator | criado |
| paradigm_decision.md | paradigm_advisor | criado |
| target_business_rules.md | curator | criado |
| discard_log.md | curator | criado |
| migration_strategy.md | strategist | criado |
| risk_register.md | strategist | criado |
| cutover_plan.md | strategist | criado |
| topology_decision.md | designer (Fase 1) | criado |
| target_architecture.md | designer | criado |
| target_domain_model.md | designer | criado |
| target_data_model.md | designer | criado |
| data_migration_plan.md | designer | criado |
| screen_modernization_decision.md | screen_translator | criado |
| target_screens.md | screen_translator | criado |
| screen_deviation_log.md | screen_translator | vazio |
| _reversa_sdd/screens/inventory.json | screen_translator | criado |
| _reversa_sdd/screens/golden/manifest.yaml | screen_translator | criado |
| parity_specs.md | inspector | criado |
| parity_tests/*.feature | inspector | 5 arquivos |
| ambiguity_log.md | orchestrator | consolidado |

## Bloqueadores para começar a implementação

- nenhum bloqueador — prosseguir com implementação bottom-up
- Revisar itens **REFERIDOS À CODIFICAÇÃO** em `ambiguity_log.md` durante sprints (não bloqueiam início)

## Próximos passos para o agente de codificação

1. **Internalizar paradigma**: API em camadas; solver procedural em `packages/solver/` — não reescrever backtracking.
2. **Internalizar topologia**: criar monorepo conforme esboço em `topology_decision.md`.
3. **Internalizar telas**: modo modernizado; 9 telas MVP em `target_screens.md` com 4 estados cada.
4. **Configurar repositório**: Python 3.11+, Node 20+, PostgreSQL 16, Docker Compose (`infra/`).
5. **Implementar bottom-up**: infra → schema BD → packages/solver refactor → worker → api → web.
6. **Testes desde o início**: traduzir `parity_tests/*.feature` para pytest/Playwright.
7. **Parallel Run**: antes cutover, diff xlsx CLI vs plataforma (ver `cutover_plan.md`).
8. **Migração dados**: seguir `data_migration_plan.md` (seed catálogo + import blobs).
9. **Cutover**: critérios go/no-go em `cutover_plan.md`.

## Itens auto-decididos (`--auto`)

- Estratégia Strangler Fig + Parallel Run (AUTO-003)
- Topologia modernizada (AUTO-004)
- UI modernizada greenfield (AUTO-006)
- Context vs Redux → implementador (AMB-C01)
- Ver `_reversa_sdd/migration/ambiguity_log.md § AUTO-DECIDIDOS`

## Notas finais

- PR #18 já no legado: LP/LIT/RED, SEED=3, folga_extra — solver wrap deve incluir essas versões.
- OpenAPI draft: `_reversa_sdd/openapi/calendarioprovas.yaml`
- Plataforma tasks: `_reversa_sdd/plataforma-multi-coordenador/tasks.md`
- Próximo fluxo Reversa opcional: `/reversa-reconstructor` com fonte **migração** (`reconstruction-plan.md`)
