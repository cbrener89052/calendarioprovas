# Regras de Negócio — Tarefas

- [ ] T-01, Extrair catálogo inicial da skill (IDs + descrição)
  - Origem: `calendario-provas/SKILL.md` 🟢

- [ ] T-02, Schema `RuleSetSnapshot` + migração PostgreSQL
  - Confiança: 🟡

- [ ] T-03, `RulesSelectionWizard` UI
  - Origem: user-requirements 🟡

- [ ] T-04, Integrar snapshot em `CalendarSolver`
  - Origem: `geracao-calendario` 🟡

- [ ] T-05, Implementar R-2CH no gerador
  - Origem: skill sync 2026-08-20 🔴

- [ ] T-06, Checklist verificador item 2CH
  - Confiança: 🔴

- [ ] T-07, Unificar feriados (`CalendarConstraintsService`)
  - Origem: ADR-012 🟡

Ordem: T-01 → T-02 → T-03 → T-04 → T-07 → T-05 → T-06
