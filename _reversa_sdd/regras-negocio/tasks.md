# Regras de Negócio — Tarefas

## Tarefas

- [ ] T-01 — Inventariar regras SKILL.md → CSV catálogo inicial
  - Origem: SKILL.md + domain.md
  - Confiança: 🟢

- [ ] T-02 — Marcar `implementada_solver` (incl. lacuna PR #14)
  - Origem: code-analysis, addenda PR #14
  - Confiança: 🟢

- [ ] T-03 — Implementar `RuleContext` builder
  - Origem: ADR-006
  - Confiança: 🟡

- [ ] T-04 — Migration REGRA_CATALOGO + REGRA_CONFIG + seed
  - Origem: erd-complete.md
  - Confiança: 🟡

- [ ] T-05 — API toggles CRUD
  - Confiança: 🟡

- [ ] T-06 — CRUD CUSTOMIZACAO_IA
  - Confiança: 🟢

- [ ] T-07 — Job sync skill → catálogo
  - Origem: sync-regras.md
  - Confiança: 🟡

- [ ] T-08 — Implementar RN PR #14 no solver + verificador
  - Confiança: 🔴

## Testes

- [ ] TT-01 — RuleContext com regra desativada exclui constraint
- [ ] TT-02 — Catálogo ≥30 regras com skill_ref válido

## Ordem

T-01 → T-02 → T-04 → T-03 → T-05 → T-06 → T-07 → T-08

## Lacunas (🔴)

- Escopo IA no verificador
- Schema params JSON por regra
