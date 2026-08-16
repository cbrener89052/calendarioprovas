# Geração de Calendário — Design Técnico

> Feature: `geracao-calendario` | Legado: `gerar_calendario.py` (~2135 linhas)

## Interface

### Legado (CLI)

| Entrada | Formato | Origem |
|---------|---------|--------|
| Grade horária | `GRADE_TXT` (Python hardcoded) ou estrutura importada | `gerar_calendario.py` |
| Modelo calendário | xlsx com abas por turma | `modelos/` |
| Simulados / ocupação | Células pré-preenchidas no modelo | `carregar_ocupadas()` |
| Seed | Inteiro (`SEED_PROPOSTA_3=3`) | constante |

| Saída | Formato | Destino |
|-------|---------|---------|
| Calendário Proposta 3 | xlsx | `Proposta_3_<semestre>.xlsx` |
| Relatório de trocas | markdown | stdout / arquivo `.md` |
| Turmas falhadas | lista de strings | stdout |

### Plataforma alvo (🟡)

| Método | Caminho | Entrada | Saída | Status |
|--------|---------|---------|-------|--------|
| GET | `/api/v1/intake/template` | semestre opcional | `Mascara_Entrada_Provas.xlsx` | 200 |
| POST | `/api/v1/intake/upload` | xlsx preenchido | preview `ExamCatalog` | 200 |
| POST | `/api/v1/calendars/{id}/factor` | `RuleSetSnapshot`, seed opcional | job id + progresso | 202 |
| GET | `/api/v1/calendars/{id}/factor/{jobId}` | — | status, falharam, blob urls | 200 |

**IntakeTemplateService:** gera máscara vazia (aba `catalogo`, cabeçalhos + linha exemplo);
parse upload → validação → `ExamCatalogService`. Spec: `_reversa_sdd/templates/mascara-entrada-provas-spec.md`.

**CalendarLayoutTemplate:** `Klausurplan_2026_2SEM.xlsx` versionado — aplicado em `escrever()`; não é formulário de entrada.

Componente: `CalendarSolver` em `_reversa_sdd/architecture.md`.

### Funções principais (legado 🟢)

| Símbolo | Assinatura | Retorno | Observação |
|---------|-----------|---------|------------|
| `montar_exames` | `(turma)` | `list[(disc, prof, n_tempos, periodo)]` | Deriva exames da grade |
| `slots_da_disciplina` | `(turma, disc, n_tempos)` | `list[(d, t, doador)]` | Slots candidatos + doador |
| `professor_presente_no_bloco` | `(turma, disc, prof_txt, d, t_ini, n)` | `bool` | R-P1 inviolável |
| `escada` | `(n_exames, cessoes)` | degraus limites | intervalo / tarde / G1 |
| `_tentar` | `(turma, seed, limites, estado)` | `(ok, resultado)` | Nó do backtracking |
| `resolver` | `(turma, seed, pré-ocupação)` | `(ok, res, max_g1, tarde, intervalo)` | Por turma |
| `resolver_par` | `(a, b, seed, cessoes)` | alocações + comuns | Turmas irmãs |
| `montar_proposta` | `(seed, flags relaxamento)` | `(alocacoes, falharam)` | Orquestrador |
| `Cessoes` | estado mutável | contadores C1–C5 | Por turma |
| `escrever` | `(proposta_num, alocacoes)` | void | Persiste xlsx |
| `relatorio` | alocações | markdown | Cessões |

## Fluxo Principal

1. **Carregar ocupação** — `carregar_ocupadas()` lê células já preenchidas (simulados, datas fixas). 🟢
2. **Montar proposta** — `montar_proposta(seed)` itera pares irmãos via `calcular_pares_irmas()` / `classificar_par()`. 🟢
3. **Resolver par** — `resolver_par()` executa backtracking conjunto `_tentar_par` respeitando coordenação R-IRM. 🟢
4. **Resolver turma** — Para cada turma restante, `resolver()` → `_tentar()` com ordenação MRV e heurísticas de preferência. 🟢
5. **Escada interna** — Dentro do solver: relaxa limites de intervalo → tarde → grupo 1 conforme `escada()`. 🟢
6. **Escada externa** — Se turmas falham: relaxa C4 → C3 → incrementa `folga_extra` (loop até 12×). 🟢
7. **Persistir** — `escrever(3, ...)` + `relatorio(...)`. 🟢

Referência: `_reversa_sdd/flowcharts/geracao-calendario.md`.

## Fluxos Alternativos

- **Par com aula combinada (mesmo slot na grade):** `classificar_par` retorna tipo que dispensa coordenação extra entre irmãs. 🟢
- **Par com Inglês no Grupo 1:** exceção permite 2 provas G1/semana com uma sendo Inglês (`par_g1_permitido`). 🟢
- **Filosofia / Sociologia:** coordenação entre irmãs não exige simultaneidade (verificador); gerador trata via regras de slot. 🟢
- **Esgotamento de nós:** `MAX_NOS` / `MAX_NOS_CESSAO` abortam ramo; contribui para falha da turma. 🟢
- **Plataforma — regra desmarcada:** regra fora do `RuleSetSnapshot` é ignorada pelo solver (equivalente a não existir na rodada). 🟡

## Dependências

- **openpyxl** — leitura/escrita do modelo e saída xlsx. 🟢
- **Grade horária** — `GRADE_TXT` ou módulo `extracao-grade` (futuro: blob + parser). 🟢
- **Catálogo de regras** — skill + constantes; futuro: `RulesCatalogService` + snapshot por sessão. 🟡
- **verificacao-calendario** — validação pós-geração independente (releitura xlsx). 🟢
- **exportacao-relatorios** — derivados do xlsx gravado, não da memória do solver. 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Backtracking MRV + preferências locais | `_tentar` ordenação por slots | 🟢 |
| Seed fixa para operação corrente | `SEED_PROPOSTA_3=3` | 🟢 |
| Relaxamento em duas escadas (interna + externa) | `escada()` + loop `main()` | 🟢 |
| Apenas Proposta 3 | `main` L2066, ADR-001 | 🟢 |
| Grade 2º sem 2026 hardcoded | `GRADE_TXT` em `gerar_calendario.py` | 🟢 |
| RuleSet injetável na plataforma | user-requirements + architecture | 🟡 |

## Estado Interno

| Estado | Campos | Onde |
|--------|--------|------|
| `Cessoes` | contadores regra 3/4, folga, histórico semanal | instância por turma durante `montar_proposta` |
| Backtracking | pilha de alocações parciais, nós visitados | `_tentar`, `_tentar_par` |
| Pré-ocupação | simulados, `FORCAR_DATA` | mapa carregado de xlsx |
| RuleSetSnapshot (futuro) | regras ativas + flags flex | PostgreSQL `rule_set_snapshots` |

## Observabilidade

- **Legado:** prints de progresso, turmas falhadas, iterações de relaxamento no stdout. 🟢
- **Alvo:** job async com logs estruturados (seed, iteração, regra relaxada, turma, nós explorados). 🟡

## Riscos e Lacunas

- 🔴 Divergência `FERIADOS` (datas) vs `BLOQUEIOS` (semana/dia) pode gerar calendário que falha no verificador.
- 🟡 Extração futura da grade para BD/blob — hoje hardcode impede multi-semestre sem deploy de código.
- 🟡 Tempo de execução não limitado por timeout global, apenas por contagem de nós.
