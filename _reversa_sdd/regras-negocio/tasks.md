# Regras de Negócio — Tarefas

- [ ] T-01, Extrair catálogo inicial da skill (IDs + descrição)
  - Origem: `calendario-provas/SKILL.md` 🟢

- [ ] T-02, Schema `RuleSetSnapshot` + migração PostgreSQL
  - Confiança: 🟡

- [ ] T-03, `RulesSelectionWizard` UI
  - Origem: user-requirements 🟡

- [ ] T-04, Integrar snapshot em `CalendarSolver`
  - Origem: `geracao-calendario` 🟡

- [ ] ~~T-05, Implementar R-2CH no gerador~~ — **Cancelado** (Won't ADR-015)

- [ ] ~~T-06, Checklist verificador item 2CH~~ — **Manual** (Won't ADR-015)

- [ ] T-05b, `EnemWeekConfigPanel` + persistência + catálogo R-ENEM
  - Origem: ADR-015 🟢

- [ ] T-06b, Verificador violação ENEM (disciplina fora da janela)
  - Confiança: 🟢

- [ ] T-07, Unificar feriados (`CalendarConstraintsService`)
  - Origem: ADR-012 🟡

Ordem: T-01 → T-02 → T-03 → T-04 → T-05b → T-06b → T-07
