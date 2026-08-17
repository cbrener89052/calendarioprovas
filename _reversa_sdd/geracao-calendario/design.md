# Geração de Calendário — Design Técnico

> Fase 4 Redator. Base: `gerar_calendario.py`, `_reversa_sdd/code-analysis.md`, `flowcharts/geracao-calendario.md`.

## Interface

### CLI (legado)

| Símbolo | Assinatura | Retorno | Observação |
|---------|-----------|---------|------------|
| `main` | `()` | `void` | Entry point; orquestra carga, proposta, escrita |
| `montar_proposta` | `(seed, folga, sem_regra3, sem_regra4)` | `(alocacoes, falharam)` | Loop de afrouxamento |
| `resolver` | `(turma, seed)` | `(ok, res, g1, tarde, cruzadas)` | Backtracking por turma |
| `resolver_par` | `(t1, t2, seed)` | similar | Turmas irmãs primeiro |
| `Cessoes` | `(turma, folga)` | class | Estado de cessões por disciplina |

### Entidades principais

| Entidade | Campos-chave | Origem |
|----------|--------------|--------|
| `Grade` | turma, dia, tempo, disciplina, professor | Grade-base Python/dict |
| `Alocacao` | semana, dia, tempo, disciplina, n_tempos | Resultado do solver |
| `Cessoes` | contadores por disciplina, histórico de blocos | Estado mutável durante busca |

### API futura (plataforma) 🟡

| Método | Caminho | Entrada | Saída |
|--------|---------|---------|-------|
| POST | `/api/v1/semestres/{id}/gerar` | `{ proposta: 3, seed?: int }` | `{ job_id }` |
| GET | `/api/v1/jobs/{id}` | — | `{ status, calendario_id?, erros? }` |

## Fluxo Principal

1. **Carga** — Ler ocupadas do modelo xlsx, grades hardcoded, simulados, feriados, semanas vetadas 🟢
2. **montar_proposta** — Inicializar com `seed=SEED_PROPOSTA_3 (7)`, folga máxima 🟢
3. **Pares irmãos** — `resolver_par` para 10C1/10C2, 11C1/11C2, 12C1/12C2 antes das demais 🟢
4. **Por turma** — `resolver` → `_tentar` embaralha exames (seeded), pré-computa `slots_da_disciplina` 🟢
5. **Cessão** — Para cada slot, `Cessoes.pode_ceder` → `aplicar`; backtrack com `desfazer` se falhar 🟢
6. **Afrouxamento** — Se falhar: relaxar regra 4 → regra 3 → tetos; reiniciar `montar_proposta` 🟢
7. **Saída** — `escrever` xlsx 8 abas + relatório trocas + `detectar_regras_relaxadas` 🟢

## Fluxos Alternativos

- **MAX_NOS esgotado:** Teto `MAX_NOS=60000` ou `MAX_NOS_CESSAO=5000`; termina com disciplinas em `falharam`; não grava xlsx parcial 🟢 (`gerar_calendario.py:657-664,1082`)
- **FORCAR_DATA:** Datas forçadas não participam de relaxamento 🟢
- **Grupo 1:** Mat, DaF, Port/LP-LIT-RED, Ing não coincidem na mesma semana — checado em `_tentar` 🟢
- **Prova combinada LP/LIT/RED:** 3 tempos consecutivos, preferência manhã 🟢
- **Regra 4 relaxada:** Cessão permitida apenas em semanas **posteriores** à prova da disciplina cedente 🟢

## Dependências

- **openpyxl** — Leitura modelo, escrita calendário 🟢
- **Grade-base** — Dict Python (hoje em arquivo; futuro BD/blob) 🟢
- **SKILL.md / RuleContext** — Fonte de regras; futuro toggles ADR-006 🟡
- **verificar_calendario** — Consumidor downstream do xlsx gerado 🟢

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Apenas Proposta 3 (cessão) | ADR-001, constantes | 🟢 |
| `SEED_PROPOSTA_3 = 3` | PR #18 | 🟢 |
| `LIMITE_LPLITRED_CONSELHO = 9` | `gerar_calendario.py:386` | 🟢 |
| `folga_extra` por turma | `montar_proposta` | 🟢 |
| Slots pré-computados antes da recursão | `slots_da_disciplina` | 🟢 |
| Pares irmãos resolvidos primeiro | `montar_proposta` ordem | 🟢 |
| Constantes in-file vs config externa | Sem `requirements.txt`, sem YAML | 🟢 |

## Estado Interno

- **Cessoes:** Por turma, rastreia cessões por disciplina, semanas sem contato, percentual acumulado, flags regra 3/4 relaxadas 🟢
- **Ocupadas:** Mapa células já usadas (simulados, provas alocadas) 🟢
- **Backtracking stack:** Alocações parciais revertidas via `desfazer` 🟢

## Observabilidade

- **Legado:** stdout com progresso e avisos; sem logging estruturado 🟢
- **Futuro:** Job worker com logs por `job_id`, métricas de nós visitados e tempo 🟡

## Riscos e Lacunas

- 🟡 Hardcode impede multi-segmento sem refactor para `RuleContext` + GRUPO
- 🟡 Acoplamento verificador importa constantes do gerador
- 🟡 Customização IA (ADR-006) não entra no solver — camada separada
