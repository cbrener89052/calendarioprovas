# Exportação de Relatórios — Tarefas de Implementação

## Pré-requisitos

- [ ] Proposta_3 xlsx golden file
- [ ] Parser células compartilhado com verificador 🟡

## Tarefas

- [ ] T-01, `exportar_tabelas_turma` → módulo + teste golden
  - Origem: `exportar_tabelas_turma.py`
  - Confiança: 🟢

- [ ] T-02, `exportar_tempos_cedidos`
  - Origem: `exportar_tempos_cedidos.py`
  - Confiança: 🟢

- [ ] T-03, `exportar_relatorio_trocas` (md + xlsx 3 abas)
  - Origem: `exportar_relatorio_trocas.py`
  - Critério: paridade linhas cessão com `gerar_calendario.relatorio()`
  - Confiança: 🟢

- [ ] T-04, `exportar_provas_por_professor`
  - Origem: `exportar_provas_por_professor.py`
  - Confiança: 🟢

- [ ] T-05, Extrair `parse_provas_xlsx()` compartilhado
  - Origem: DT-07 architecture
  - Confiança: 🟡

- [ ] T-06, `ReportExporter` API + blob storage
  - Confiança: 🟡

- [ ] T-07, Integrar `DonorEmailService.preview` com export trades
  - Origem: ADR-007
  - Confiança: 🟡

- [ ] T-08, `ReportExporter.rulesPdf` — PDF regras Must plataforma v1
  - Origem: ADR-015 5c; catálogo + RuleSetSnapshot
  - Critério: download PDF; paridade conteúdo com referência institucional 🟡
  - Confiança: 🟢

## Ordem

T-05 → T-01..T-04 → T-06 → T-07 → T-08
