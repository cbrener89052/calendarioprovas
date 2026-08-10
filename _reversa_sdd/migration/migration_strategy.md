---
schemaVersion: 1
generatedAt: 2026-08-10T02:05:00Z
reversa:
  version: "1.2.58"
kind: migration_strategy
producedBy: strategist
---

# Migration Strategy

> Estratégias avaliadas. Recomendada: **Strangler Fig + Parallel Run (solver)**.

## Contexto sintetizado

| Dimensão | Valor |
|----------|-------|
| Tamanho legado | ~7 módulos Python, ~1900 linhas solver, sem BD |
| Apetite derivado | transformational (paradigm_decision) |
| Gap paradigma | Alto (CLI monolítico → API + worker + web) |
| Restrições | Preservar solver Python; deploy híbrido |
| Regras críticas | Proposta 3, cessão, LP/LIT/RED, verificador |

## Estratégias avaliadas

### Estratégia A: Strangler Fig
- **Descrição**: Envolver solver legado em `packages/solver/`; API/worker substituem CLI incrementalmente.
- **Quando aplica**: Sistema funcional que não pode regredir; roteamento API vs CLI durante transição.
- **Custo**: médio | **Risco**: baixo | **Tempo**: médio
- **Adequação ao apetite**: Alta — permite evolução sem reescrever algoritmo.
- **Prós**: Reuso Python; deploy parcial; rollback por borda.
- **Contras**: Duplicação temporária CLI + plataforma durante Parallel Run.

### Estratégia B: Big Bang
- **Descrição**: Novo monorepo completo; desliga CLI após go-live.
- **Quando aplica**: Sistemas pequenos, janela única.
- **Custo**: baixo | **Risco**: alto | **Tempo**: curto
- **Adequação**: Média — solver complexo aumenta risco de paridade.
- **Contras**: Sem prova incremental; falha no cutover bloqueia semestre.

### Estratégia C: Parallel Run (fase de validação)
- **Descrição**: Rodar CLI e worker plataforma com mesmas entradas; comparar xlsx byte-a-byte.
- **Quando aplica**: Lógica combinatória crítica; prova de equivalência.
- **Custo**: alto | **Risco**: médio | **Tempo**: médio
- **Adequação**: Alta como **fase** dentro do Strangler.
- **Prós**: Confiança antes do cutover; alinhado a métricas do brief.
- **Contras**: Esforço duplicado de execução durante validação.

## Comparativo

| Critério | Strangler | Big Bang | Parallel Run |
|---|---|---|---|
| Custo | médio | baixo | alto |
| Risco | baixo | alto | médio |
| Tempo | médio | curto | médio |
| Aderência apetite | alta | média | alta (fase) |
| Compat. mudança paradigma | alta | baixa | alta |

## Recomendação do Strategist

- **Estratégia recomendada**: **A — Strangler Fig**, com **fase C — Parallel Run** obrigatória para solver/verificador antes do cutover.
- **Justificativa**: Gap alto de paradigma + solver combinatório crítico exige prova de paridade (brief: "equivalente ao CLI"). Strangler isola `packages/solver/` sem reescrita. Parallel Run valida xlsx + verificador OK antes de desligar CLI.

## Sinais de alerta

- Mudança procedural → serviços: externalizar constantes antes de multi-tenant completo.
- Sem testes automatizados legado (G-M05): characterization tests derivados de `parity_tests/`.

## Decisão humana

- **Estratégia escolhida**: A (Strangler Fig + Parallel Run solver)
- **Quem decidiu**: auto (`--auto`, orquestrador cloud)
- **Quando**: 2026-08-10T02:05:00Z
- **Justificativa**: Default recomendado; alinhado a brief e paradigm_decision.
