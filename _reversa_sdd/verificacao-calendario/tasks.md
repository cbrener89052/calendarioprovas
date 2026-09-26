# Verificação de Calendário — Tarefas

## Pré-requisitos

- [ ] xlsx calendário gerado
- [ ] Grade-base e constantes (shared config module)

## Tarefas

- [ ] T-01 — Parser de células → eventos (prova, simulado, LP/LIT/RED)
  - Origem: `verificar_calendario.py:main`
  - Critério: Parse idêntico ao gerador para 8 turmas referência
  - Confiança: 🟢

- [ ] T-02 — Checks distribuição temporal (3/sem, 1/dia, 4 semanas)
  - Origem: loops de validação no main
  - Critério: Casos positivo/negativo automatizados
  - Confiança: 🟢

- [ ] T-03 — Checks cessão vs grade-base
  - Origem: cruzamento grade + xlsx
  - Critério: Detecta cessão véspera como erro
  - Confiança: 🟢

- [ ] T-04 — Check LP/LIT/RED 10 dias conselho
  - Origem: PR #14, skill
  - Critério: Erro quando <10 dias
  - Confiança: 🔴

- [ ] T-05 — Extrair módulo `rules/` compartilhado com gerador
  - Origem: acoplamento import
  - Critério: Verificador não importa gerador inteiro
  - Confiança: 🟡

- [ ] T-06 — Endpoint POST verificar (plataforma)
  - Origem: architecture.md
  - Critério: Integrado ao pipeline pós-job
  - Confiança: 🟡

## Tarefas de Teste

- [ ] TT-01 — xlsx referência 2sem2026 passa sem erros
- [ ] TT-02 — xlsx sintético com 4 provas/semana falha
- [ ] TT-03 — cessão véspera falha sempre

## Ordem Sugerida

T-05 → T-01 → T-02 → T-03 → T-04 → T-06

## Lacunas (🔴)

- Escopo customização IA no verificador
- Validação cores ARGB
