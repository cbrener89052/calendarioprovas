# Análise técnica de código — calendarioprovas

> Gerado pelo Arqueólogo (Reversa) em 2026-08-15  
> Nível: **completo** | Organização das specs: **feature**

## Visão geral

Sistema **Python CLI monolítico** para montar calendários de provas da Escola Alemã Corcovado. O núcleo é `gerar_calendario.py` (~2135 linhas): solver de restrições com backtracking, coordenação entre turmas irmãs e limites de cessão (Proposta 3). Scripts satélite validam e exportam relatórios a partir das planilhas gravadas.

**Stack:** Python 3, openpyxl, PyMuPDF (extração PDF), Tesseract (OCR legado 2025), fpdf (PDF de regras).

**Evolução planejada:** plataforma web multi-coordenador (FastAPI + PostgreSQL) — ver módulo `plataforma-multi-coordenador`.

---

## Módulo: geracao-calendario

**Arquivos:** `gerar_calendario.py`  
**Propósito:** 🟢 Gerar proposta de calendário de provas, escrever xlsx e relatório de trocas.

### Fluxo de controle

1. `main()` → `carregar_ocupadas()` lê células pré-ocupadas do modelo
2. `montar_proposta(seed, ...)` — pipeline principal
3. Para cada par irmão: `resolver_par()` → backtracking conjunto (`_tentar_par`)
4. Por turma: `resolver()` → backtracking individual (`_tentar`)
5. Se falhar: relaxa regra 4 → regra 3 → `folga_extra` (até 12 iterações)
6. `escrever(3, alocacoes)` + `relatorio(...)`

### Funções principais

| Função | Parâmetros | Retorno | Confiança |
|---|---|---|---|
| `montar_exames(turma)` | turma | `list[(disc, prof, n_tempos, periodo)]` | 🟢 |
| `slots_da_disciplina(turma, disc, n_tempos)` | turma, disc, n | `list[(d, t, doador)]` | 🟢 |
| `professor_presente_no_bloco(...)` | turma, disc, prof_txt, d, t_ini, n | `bool` | 🟢 |
| `escada(n_exames, cessoes)` | n, Cessoes\|None | degraus `(max_intervalo, max_tarde, max_g1)` | 🟢 |
| `_tentar(...)` | turma, seed, limites, estado | `(ok, resultado)` | 🟢 |
| `resolver(...)` | turma, seed, pré-ocupação | `(ok, res, max_g1, tarde, intervalo)` | 🟢 |
| `resolver_par(a, b, seed, cessoes)` | duas turmas | alocações + `comuns` | 🟢 |
| `montar_proposta(seed, ...)` | seed, flags relaxamento | `(alocacoes, falharam)` | 🟢 |
| `Cessoes` | turma, folga, regra3/4 | estado mutável de cessões | 🟢 |

### Algoritmos

- **Backtracking MRV:** ordena exames por menos slots; heurísticas de preferência (intervalo, tarde, grupo 1, alternância de doador)
- **Escada dupla:** (A) dentro do solver — intervalo → tarde → grupo 1; (B) no `main()` — regra 4 → regra 3 → teto de cessão por turma
- **Pares irmãos:** `calcular_pares_irmas()` deriva pares por regex `série+letra+número`; `classificar_par()` distingue aula combinada vs coordenação
- **Orçamento de nós:** `MAX_NOS=60000`, `MAX_NOS_CESSAO=5000`; seed fixa `SEED_PROPOSTA_3=3`

### Regras embutidas (amostra)

| Regra | Local | Confiança |
|---|---|---|
| Máx. 3 avaliações/semana | `_tentar` L1144 | 🟢 |
| Grupo 1 (exc. par com Inglês) | L1152, `par_g1_permitido` | 🟢 |
| Distância mín. 4 semanas entre provas | `DISTANCIA_MIN_MESMA_DISC` | 🟢 |
| Presença do professor no bloco | L1368 | 🟢 |
| Cessão regras 1–5 | classe `Cessoes` L850 | 🟢 |
| Só Proposta 3 gerada | `main` L2066 | 🟢 |

---

## Módulo: verificacao-calendario

**Arquivos:** `verificar_calendario.py`  
**Propósito:** 🟢 Checklist automático relendo xlsx gravado (não confia no gerador).

### Fluxo

`main()` → importa `gerar_calendario as G` → lê `Proposta_3_...xlsx` → itens 0–11 → stdout PROBLEMA/AVISO.

### Lacuna arqueológica 🟡

`FERIADOS` (datas absolutas) vs `BLOQUEIOS` (semana/dia) em `gerar_calendario.py` — duas representações que exigem sincronização manual (caso 02/11 documentado na skill).

`COORDENACAO_EXCECAO` existe só no verificador — Fil/Soc isentas de coincidência entre irmãs.

---

## Módulo: exportacao-relatorios

**Arquivos:** `exportar_tabelas_turma.py`, `exportar_tempos_cedidos.py`, `exportar_relatorio_trocas.py`, `exportar_provas_por_professor.py`, `exportar_regras_pdf.py`

**Propósito:** 🟢 Derivar relatórios da planilha final (princípio: releitura, não memória do solver).

| Script | Saída |
|---|---|
| `exportar_tabelas_turma` | `Tabela_Provas_por_Turma_Proposta_3.xlsx` |
| `exportar_tempos_cedidos` | `Relatorio_Tempos_Cedidos_Proposta_3.xlsx` |
| `exportar_relatorio_trocas` | `.md` + `.xlsx` (3 abas) |
| `exportar_provas_por_professor` | `Provas_por_Professor_Proposta_3.xlsx` |
| `exportar_regras_pdf` | `referencia/Regras_Negocio_...pdf` (estático) |

Todos hardcoded para **Proposta 3**.

---

## Módulo: extracao-grade

**Arquivos:** `esqueleto_grade_2025.py`, `extrair_grade_2025.py`, `limpar_grade_2025.py`, `extrair_grade_1semestre.py`, `horarios2025/*.py`

**Propósito:** 🟢 Converter PDFs de horário Untis em estruturas Python importáveis.

- **2025:** geometria PDF + OCR Tesseract → `GRADE_BRUTA_2025` → `limpar_grade_2025` → `GRADE_2025`
- **1º sem 2026:** PDF com texto → `GRADE_1SEM` via hora de início

**Nota:** grade ativa do 2º sem 2026 está **hardcoded** em `gerar_calendario.GRADE_TXT`, não extraída por script.

---

## Módulo: analise-historica

**Arquivos:** `analisar_1semestre.py`, `analisar_2sem_2025.py`, `contar_2sem_2025.py`, `comparar_semestres.py`

**Propósito:** 🟢 Análise retrospectiva de cessões e benchmark entre semestres.

- `analisar_1semestre` → cessões reais 1º sem 2026 vs `GRADE_1SEM`
- `contar_2sem_2025` → reconstrói tempos usados em 2025 (só duração `(N)` no xlsx)
- `comparar_semestres` → % cessões 1º sem ocorrido vs Proposta 3

---

## Módulo: regras-negocio

**Arquivos:** `.claude/skills/calendario-provas/SKILL.md` (espelho: `.agents/skills/calendario-provas/SKILL.md`)  
**Fonte viva registrada em:** `.reversa/context/sources.json` → `skill-calendario-provas`

**Propósito:** 🟢 Fonte formal das regras de distribuição, cessão e entregáveis (~1010 linhas).

Duplicidade intencional hoje: skill (documentação + agente) + código (execução). **Prioridade de leitura:** skill → código → snapshot `_reversa_sdd/`. Ver `.reversa/context/sync-regras.md`.

**Catálogo para UI futuro (seleção de regras):** seções principais da skill — Passo 0 (15 perguntas), Regras de distribuição, Limites de cessão, Entregáveis, Checklist de verificação.

---

## Módulo: plataforma-multi-coordenador

**Arquivos:** 🔴 LACUNA — não implementado. Requisitos em `.reversa/context/user-requirements.md`.

**Propósito previsto:** 🟡 FastAPI + PostgreSQL + login (5 coordenadores); persistência de entradas/saídas; deploy nuvem + Docker on-prem.

**Feature nova (2026-08-15):** tela de seleção de regras antes da fatoração (geração automática), com defaults (todas ativas), regras inegociáveis na mesma tela, regras novas fixas ou por sessão, e revisão antes de fechar o horário.

**Feature nova (2026-08-15):** envio **manual** de e-mail aos professores **doadores** de tempo (cessões), disparado pelo coordenador quando o calendário estiver seguro — **não** a cada refração. Dados espelham `Relatorio_trocas_de_tempo` (`exportar_relatorio_trocas.py`). Ver `.reversa/context/user-requirements.md`.

---

## Resumo quantitativo

| Métrica | Valor |
|---|---|
| Scripts Python (projeto) | 16 |
| Módulos analisados | 7 |
| Turmas no gerador | 8 (9C–12C) |
| Linhas `gerar_calendario.py` | 2135 |
| Testes automatizados | 0 |
| Banco de dados | Ausente |
