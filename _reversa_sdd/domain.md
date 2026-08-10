# Domínio — calendarioprovas

> Gerado pelo Detetive (Reversa), doc_level=completo.  
> Fontes: skill `calendario-provas`, código, git history, adendos `_reversa_sdd/addenda/`.

---

## Glossário

| Termo | Definição | Confiança |
|---|---|---|
| **Turma C** | Classe do ramo C (9C1–12C2), 8 turmas no 2º sem 2026 | 🟢 |
| **Tempo** | Período de aula numerado 1–11 (7h15–15h55) | 🟢 |
| **Grade-base** | Horário semanal `(dia, tempo) → (disciplina, professor)` | 🟢 |
| **Proposta** | Versão de calendário gerada; hoje só **Proposta 3** (cessão) | 🟢 |
| **Rodada** | P1 ou P2 — metade do semestre de provas | 🟢 |
| **Grupo 1** | Mat, DaF, Port/LP-LIT-RED, Ing — não coincidem na mesma semana | 🟢 |
| **Turmas irmãs** | Par 10C1/10C2, 11C1/11C2, etc. — coordenação se mesmo professor | 🟢 |
| **Cessão** | Tempo de aula de disciplina A usado para prova de disciplina B | 🟢 |
| **Simulado/AG** | Avaliação global fixa (AG9, AG10, S3-11…) — 2º–7º tempo, amarelo | 🟢 |
| **Semana vetada** | Semana de conselho de classe — sem provas normais | 🟢 |
| **Coordenador** | Usuário futuro da plataforma (5 contas) | 🟡 |
| **Segmento** | Escopo escolar do coordenador (turmas, regras, parâmetros) | 🟢 |
| **GRUPO** | Agrupamento customizável de turmas: nome, início/fim semestre, 2ª chamada, conselho | 🟢 |
| **Grupo 1** | Mat, DaF, Port/LP-LIT-RED, Ing — regra de distribuição (≠ GRUPO acima) | 🟢 |
| **Regra codificada** | Restrição no solver; toggle ativo/inativo | 🟢 |
| **Customização IA** | Preferência/exceção interpretada por IA, sem alterar código | 🟢 |
| **Semestre letivo** | Unidade de trabalho (ex.: 2º sem 2026) | 🟢 |

---

## Regras de domínio (consolidadas)

### Distribuição temporal

1. Máx. **3 avaliações/semana** por turma (simulado 2 dias = 1) 🟢
2. **1 prova/dia** por turma 🟢
3. **Distância mínima 4 semanas** entre 2 provas da mesma disciplina (por número de semana) 🟢
4. Provas dentro do **período do GRUPO** da turma (início/fim semestre configuráveis), sem feriados/semana vetada de conselho 🟢
5. **LP/LIT/RED** (10–12): 3 tempos, 1ª ou 2ª semana de cada rodada 🟢
6. **LP/LIT/RED ≥10 dias** antes do início da semana vetada de conselho 🟢 skill + código (PR #18)
7. **Intervalo recreio**: proibido cruzar 3+4 ou 5+6; exceção com destaque laranja 🟢

### Cessão de aula (Proposta 3)

| # | Regra | Rigidez |
|---|---|---|
| 1 | 2–3 aulas/sem → máx. 2 cessões (3 Hist/Geo/GL) | Dura |
| 2 | 1 aula/sem → não cede | Dura |
| 3 | Não 2 semanas seguidas sem contato | Relaxável (2º) |
| 4 | Não ceder vésperas da própria prova; relaxada = só **depois** | Relaxável (1º) |
| 5 | Teto **11%** das aulas programadas | Dura |

**Escada de afrouxamento:** regra 4 (por turma) → regra 3 (por turma) → tetos +1. Datas `FORCAR_DATA` **nunca** relaxam 🟢

### Entregáveis obrigatórios

- Calendário xlsx (8 abas)
- Relatório trocas de tempo (+ seção **Regras relaxadas**)
- Tabela-resumo por turma
- Relatório tempos cedidos (Proposta 3)

---

## Regras implícitas (extraídas do código)

| Regra | Evidência | Confiança |
|---|---|---|
| Semente `SEED_PROPOSTA_3 = 3` após PR #18 (era 7) | `gerar_calendario.py:678` | 🟢 |
| `LIMITE_LPLITRED_CONSELHO = 9` | `gerar_calendario.py:386` | 🟢 |
| `folga_extra` por turma na escada cessão | `montar_proposta` | 🟢 |
| Falha `resolver_par` entra em `falharam` | PR #18 | 🟢 |
| Orçamento `MAX_NOS` limita backtracking (~600 nós/s) | comentário + constante | 🟢 |
| Slots pré-computados por disciplina antes da busca | `slots_da_disciplina` | 🟢 |
| Pares irmãos resolvidos **antes** das turmas individuais | `montar_proposta` | 🟢 |
| Verificador lê xlsx gravado, não memória do gerador | `verificar_calendario.py` docstring | 🟢 |
| Exportadores cruzam xlsx + grade-base para cessões | `exportar_tempos_cedidos.py` | 🟢 |
| Constantes hardcoded — sem config externa | Scout + código | 🟢 |

---

## Lacunas 🔴

| Lacuna | Impacto |
|---|---|
| ~~LP/LIT/RED 10 dias~~ | ✅ PR #18 |
| Verificação de cores ARGB opacas | Skill pede; verificador parcial |
| RBAC por segmento | 🟢 user-requirements 2026-08-09 |
| Motor regras toggles + IA | 🟢 ADR-006 |
| `requirements.txt` ausente | Dependências implícitas (openpyxl, fpdf, pymupdf) |

---

## Hierarquia de fontes (domínio)

1. `.claude/skills/calendario-provas/SKILL.md`
2. `gerar_calendario.py` + `verificar_calendario.py`
3. `referencia/estado_2sem_2026.md`
4. `_reversa_sdd/code-analysis.md` (snapshot)

Ver `.reversa/context/sources.json`.
