# Geração de Calendário — Tarefas de Implementação

> Feature: `geracao-calendario` | Rastreabilidade ao legado `gerar_calendario.py`

## Pré-requisitos

- [ ] Modelo xlsx e convenções de abas documentados em `_reversa_sdd/data-dictionary.md`
- [ ] Grade horária disponível (hardcoded ou importada de `extracao-grade`)
- [ ] Catálogo de regras mapeado (feature `regras-negocio`) para plataforma
- [ ] openpyxl instalado / declarado em dependências do projeto alvo

## Tarefas

- [ ] T-01, Extrair constantes de domínio (turmas, feriados, bloqueios, `FORCAR_DATA`, limites G1)
  - Origem no legado: `gerar_calendario.py` (topo do arquivo)
  - Critério de pronto: módulo `domain/constants.py` importável sem efeitos colaterais
  - Confiança: 🟢

- [ ] T-02, Implementar `montar_exames` e `slots_da_disciplina`
  - Origem no legado: `gerar_calendario.py` (~funções de montagem)
  - Critério de pronto: lista de exames bate com amostra de 3 turmas do semestre de referência
  - Confiança: 🟢

- [ ] T-03, Implementar `professor_presente_no_bloco` (R-P1)
  - Origem no legado: `gerar_calendario.py` L1368
  - Critério de pronto: casos positivo/negativo com turma irmã cobertos
  - Confiança: 🟢

- [ ] T-04, Implementar classe `Cessoes` (regras C1–C5)
  - Origem no legado: `gerar_calendario.py` L850
  - Critério de pronto: unit tests para teto 11%, regra semanal e véspera
  - Confiança: 🟢

- [ ] T-05, Implementar `_tentar` / `resolver` com MRV e heurísticas
  - Origem no legado: `gerar_calendario.py` L1144+
  - Critério de pronto: mesma seed 3 reproduz alocação legada para turma piloto
  - Confiança: 🟢

- [ ] T-06, Implementar `calcular_pares_irmas`, `classificar_par`, `resolver_par`
  - Origem no legado: funções de par irmão
  - Critério de pronto: par 10C1/10C2 classificado e resolvido conforme skill
  - Confiança: 🟢

- [ ] T-07, Implementar `montar_proposta` com escada externa (12 iterações)
  - Origem no legado: `montar_proposta` + loop em `main()`
  - Critério de pronto: cenário de falha dispara relaxamento na ordem C4→C3→folga
  - Confiança: 🟢

- [ ] T-08, Implementar `carregar_ocupadas`, `escrever`, `relatorio`
  - Origem no legado: funções de I/O xlsx
  - Critério de pronto: xlsx gerado abre no Excel; relatório lista cessões do golden file
  - Confiança: 🟢

- [ ] T-09, Respeitar limites `MAX_NOS` e `MAX_NOS_CESSAO`
  - Origem no legado: constantes no solver
  - Critério de pronto: grafo artificial grande termina sem hang
  - Confiança: 🟢

- [ ] T-10, Injetar `RuleSetSnapshot` no solver (plataforma)
  - Origem no legado: `.reversa/context/user-requirements.md`
  - Critério de pronto: desmarcar C4 impede relaxamento da regra 4
  - Confiança: 🟡

- [ ] T-11, Expor endpoint POST `/calendars/{id}/factor` assíncrono
  - Origem no legado: `_reversa_sdd/architecture.md#CalendarSolver`
  - Critério de pronto: job retorna blob url do xlsx + lista falharam
  - Confiança: 🟡

## Tarefas de Teste

- [ ] TT-01, Golden test: seed 3 + entradas referência → diff mínimo com `Proposta_3` legado
- [ ] TT-02, Turma impossível → aparece em `falharam` após 12 relaxamentos
- [ ] TT-03, R-P1: alocação sem professor sempre rejeitada
- [ ] TT-04, RuleSet: regra desativada não é avaliada nem relaxada

## Tarefas de Migração de Dados

- [ ] TM-01, Importar grade hardcoded `GRADE_TXT` para tabela/blob por semestre/coordenador
- [ ] TM-02, Versionar snapshots de `RuleSet` ligados a cada fatoração

## Ordem Sugerida

1. T-01 → T-04 (domínio e cessões)
2. T-05 → T-07 (solver core)
3. T-06 (pares irmãos)
4. T-08 (I/O)
5. T-09, TT-01 a TT-03 (paridade legado)
6. T-10 → T-11 (plataforma)

## Lacunas Pendentes (🟡)

- T-13: ENEM configurável (`EnemWeekConfig` → solver) — Must ADR-015
- Unificação `FERIADOS` vs `BLOQUEIOS` antes de TT-01
- Timeout global além de contagem de nós na API

- [ ] ~~T-12 R-2CH~~ — **Cancelado** (Won't — ADR-015)

- [ ] T-13, Implementar constraints ENEM configuráveis
  - Origem: ADR-015 + `ui/enem-week-config-spec.md`
  - Critério de pronto: solver rejeita disciplina fora da lista da janela; verificador PROBLEMA
  - Confiança: 🟢
