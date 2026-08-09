# Análise técnica — calendarioprovas

> Gerado pelo Arqueólogo (Reversa). Organização: **por features** (`_reversa_sdd/<feature>/`).

---

## Feature: geracao-calendario

**Arquivo principal:** `gerar_calendario.py` (~1887 linhas)  
**Propósito:** Gerar proposta(s) de calendário de provas para 8 turmas C (9C1–12C2), escrever planilhas Excel e relatório de trocas de tempo.

### Entry point

```python
python gerar_calendario.py  →  main()
```

### Fluxo principal 🟢

1. `carregar_ocupadas()` — lê células já ocupadas no modelo xlsx (simulados, 2CH, etc.)
2. `montar_proposta(seed, folga, sem_regra3, sem_regra4)` — resolve alocação para 8 turmas
3. `escrever(proposta, alocacoes)` — grava xlsx por turma (mescla células, cores)
4. `relatorio(alocacoes, comuns_por_par)` — gera `Relatorio_trocas_de_tempo.md`

### Estruturas de dados centrais 🟢

| Estrutura | Tipo | Descrição |
|---|---|---|
| `GRADE_TXT` / `GRADES` | `dict[turma][dia][tempo] → (disc, prof)` | Horário-base embutido no código |
| `EXAMES` | lista por turma | Disciplinas, período, nº tempos, rótulo |
| `SIMULADOS` | dict | Datas fixas AG/S por turma |
| `BLOQUEIOS` | set `(semana, dia)` | Feriados e dias vetados |
| `FORCAR_DATA` | dict | Provas com data imposta pela coordenação |
| `PARES_IRMAS` | list `(10C1,10C2)...` | Turmas coordenadas (mesmo professor) |
| `Cessoes` | class | Estado de cessões de aula (Proposta 3) |

### Algoritmo central: backtracking 🟢

- **`resolver(turma, seed, ...)`** — backtracking com orçamento `MAX_NOS` (~600 nós/s com regras de cessão)
- **`_tentar(...)`** — tenta alocar exames respeitando folgas: intervalo recreio > grupo1 > tarde
- **`resolver_par(a, b, seed)`** — coordena provas entre turmas irmãs antes das individuais
- **`slots_da_disciplina(...)`** — pré-computa blocos válidos (dia, tempo) por prova
- **`escada(n_exames, cessoes)`** — ordena exames por dificuldade (menos slots primeiro)

### Classe `Cessoes` (Proposta 3) 🟢

Implementa regras 1–5 de cessão de aula (detalhadas na skill, seção "Limites de cessão"):

| # | Regra | Implementação |
|---|---|---|
| 1 | 2–3 aulas/sem → máx. 2 cessões (3 para Hist/Geo/GL) | `meta_cessao()` |
| 2 | 1 aula/sem → não cede | `nao_doadoras()` |
| 3 | Duas semanas seguidas sem contato | `_pares_sem_contato()` |
| 4 | Não ceder vésperas da própria prova | `pode_ceder_bloco`, `pode_alocar_exame` |
| 5 | Teto 11% das aulas programadas | `TETO_PCT_CESSAO`, `programadas_no_semestre()` |

**Regra 4 refinada (skill 2026-08):** ao afrouxar (`sem_regra4` por turma), **nunca** libera cessão na semana anterior nem no dia da prova — só **depois** do dia da aplicação. Proteção da aula de revisão é inegociável.

**Datas fixas (`FORCAR_DATA`):** inegociáveis e processadas **antes** de `resolver_par` — reservam semanas para evitar conflito com regra 4.

**Escada de afrouxamento** (`montar_proposta`): 1) regra 4 por turma → 2) regra 3 por turma → 3) tetos +1. Nunca relaxar datas fixas.

Métodos: `pode_ceder_bloco`, `pode_alocar_exame`, `aplicar`, `desfazer`, `clone`

### Relatório e regras relaxadas 🟢

- `detectar_regras_relaxadas(turma, itens)` — reconstrói violações da regra 4 a partir das alocações finais
- `relatorio()` inclui seção **"Regras relaxadas"** (tabela turma | regra | disciplina/prof | detalhe) — exigência da skill, entregável 2

### Regras embutidas no código 🟢

- Máx. 3 avaliações/semana; 1 prova/dia
- Grupo 1 (Mat, DaF, Port/LPLITRED, Ing) não coincide (exceção: 2 com Ing)
- Distância mínima 4 semanas entre provas da mesma disciplina
- Não cruzar intervalo 3+4 / 5+6 tempos (prioridade máxima)
- LP/LIT/RED turmas 10–12: 3 tempos, semanas 1–2 de cada rodada
- **LP/LIT/RED — 10 dias antes do conselho** (skill PR #14): data da prova ≥ 10 dias corridos antes do início da semana vetada (ex.: conselho 12/10 → prova não depois de 02/10). 🔴 **Lacuna no código** — ainda não implementado em `gerar_calendario.py` / `verificar_calendario.py`
- Cores ARGB 8 dígitos (`FF` + RGB) — bug histórico documentado

### Saída Excel 🟢

- Copia `Klausurplan_2026_2SEM.xlsx` → `Horario desenvolvido/Proposta_3_...xlsx`
- `_escrever_celula` — mescla bloco 3 linhas, aplica `COR_DISCIPLINA` / `COR_SIMULADO` / `DESTAQUE_INTERVALO`
- Formato célula: 3 linhas (disc-prof / sala vazia / tempos)

### Constantes de configuração 🟡

Sem arquivo externo: períodos, feriados, simulados, grades e regras estão **hardcoded** no script. Evolução futura (BD multi-coordenador) deve externalizar estes dados.

### Dependências

- `openpyxl` — leitura/escrita xlsx
- stdlib: `random`, `collections`, `copy`, `shutil`, `os`

### Complexidade

**Alta** — solver combinatório com dezenas de restrições; semente `SEED_PROPOSTA_3 = 7` fixada após testes.

---

## Feature: verificacao-calendario

**Arquivo principal:** `verificar_calendario.py` (~354 linhas)  
**Propósito:** Validar planilhas xlsx já gravadas contra o checklist da skill, sem confiar na memória do gerador.

### Entry point

```python
python verificar_calendario.py  →  main()
```

### Fluxo principal 🟢

1. Importa constantes e funções de `gerar_calendario as G` (grade, simulados, regras de cessão)
2. Para Proposta 3: abre `Horario desenvolvido/Proposta_3_Calendario_Provas_2026_2SEM.xlsx`
3. Por turma: parseia células de prova (colunas E–I, semanas 1–20)
4. Executa 11+ checks (problemas vs avisos)
5. Imprime relatório no stdout (`PROBLEMA(S)` / `OK` / `AVISO(S)`)

### Parser de células 🟢

- Ignora: `unterrichtsfrei`, cabeçalhos, `2CH`, `CC`
- Extrai: disciplina (1ª linha), tempos via regex `(\d+)º`, cor de destaque (intervalo)
- `data_da(ws, w, d)` — semana 1 = 03/08/2026 (fórmulas no xlsx)
- Simulados: regex `SIM_COD = ^(AG9|AG10|S\d-\d\d|EX\S+)`

### Checklist implementado 🟢

Espelha a skill (seção "Verificação obrigatória", ~30 itens). Principais grupos:

| Grupo | Exemplos | Tipo |
|---|---|---|
| Distribuição | máx 3/sem, 1/dia, grupo 1, distância 4 sem | problema |
| LP/LIT/RED | 3 tempos, semanas 1–2 rodada, **≥10 dias antes conselho** | problema (10 dias: 🔴 lacuna verificador) |
| Horário | tarde inevitável, intervalo + destaque laranja | aviso/problema |
| Simulados | datas oficiais, 2º–7º tempo, **amarelo exclusivo** | problema |
| Cessão P3 | regras 1–5 | problema |
| Regra 4 relaxada | cessão véspera | **aviso** |
| Regra 4 estrita | cessão **antes/no dia** da prova | **problema** (mesmo com relaxamento) |
| Turmas irmãs | professor comum → mesmo dia/tempo | problema |
| Cores | `fgColor.rgb` começa com `FF` (opaco) | 🟡 skill pede; verificador ainda foca texto |

**Distinção crítica (skill ↔ verificador):** relaxar regra 4 transforma violações **depois** da prova em aviso; violações **antes** da prova permanecem falha.

### Dependências

- `openpyxl`, `gerar_calendario` (import direto — acoplamento forte)
- stdlib: `re`, `collections`, `datetime`, `os`

### Complexidade

**Média** — lógica de validação extensa, mas linear (sem solver).

---

## Feature: exportacao-relatorios

**Arquivos:** `exportar_tabelas_turma.py`, `exportar_tempos_cedidos.py`  
**Propósito:** Gerar relatórios Excel a partir das propostas já gravadas.

### exportar_tabelas_turma.py 🟢

- **Entrada:** `Proposta_N_...xlsx` + `siglas/siglas_profs_aux_etc.xlsx`
- **Saída:** `Tabela_Provas_por_Turma_Proposta_N.xlsx` (aba/turma)
- **Colunas:** Disciplina | Professor(es) | Dia e tempos | Nº tempos
- `carregar_siglas()` — mapa sigla → nome completo
- `nomes_dos_profs()` — expande `BPad/MFo` com nomes da planilha
- `ler_provas()` — parseia células, junta simulados de 2 dias numa linha
- Formatação: cabeçalho azul, zebra, freeze, autofilter

### exportar_tempos_cedidos.py 🟢

- **Entrada:** mesma proposta + siglas
- **Saída:** `Relatorio_Tempos_Cedidos_Proposta_N.xlsx`
- **Lógica:** `cedencias_por_turma()` cruza tempos de prova com `G.GRADES` — tempo de outra disciplina = cessão
- Reutiliza `G.programadas_no_semestre()` (fonte única com gerador)
- LP/LIT/RED: família `G.COMBINA_PORT` — tempos próprios não contam como cessão
- Colunas: semanais | programadas semestre | cedidas | % (com linha Total)

### Dependências

- `openpyxl`, `gerar_calendario`, `exportar_tabelas_turma` (siglas)

### Complexidade

**Baixa–média** — leitura + transformação + escrita Excel.

---

## Feature: extracao-grade

**Arquivos:** `extrair_grade_2025.py`, `extrair_grade_1semestre.py`, auxiliares (`esqueleto_grade_2025.py`, `limpar_grade_2025.py`, `horarios2025/grade_2sem_2025*.py`)  
**Propósito:** Extrair grade horária de PDFs Untis para dict Python importável.

### extrair_grade_2025.py (2º sem 2025) 🟢

- PDF sem camada de texto → **OCR Tesseract** (400 dpi) + geometria de células
- `celula_da(x,y)` — centro da faixa vertical mais próximo (11 tempos)
- `agrupar_celulas()` — palavras OCR → `(dia, tempo) → texto`
- Saída: `horarios2025/grade_2sem_2025.py`
- Flag `--tsv` reutiliza OCR já gerado

### extrair_grade_1semestre.py (1º sem 2026) 🟢

- PDF com texto selecionável (`pymupdf.get_text("words")`)
- Tempo inferido por **hora de início** (`TEMPOS`: 7.15→1, …, 15.55→11)
- Layout célula: disciplina+hora / *professor / sala
- Saída: `horarios_1semestre/grade_1semestre.py`

### Dependências

- `pymupdf`, `tesseract` (2025), stdlib

### Complexidade

**Alta** (2025 OCR) / **Média** (2026 texto nativo)

---

## Feature: analise-historica

**Arquivos:** `analisar_1semestre.py`, `analisar_2sem_2025.py`, `comparar_semestres.py`, `contar_2sem_2025.py`  
**Propósito:** Analisar calendários passados e comparar cessões entre semestres.

### analisar_1semestre.py 🟢

- Lê `Horario modelo/Klausurplan_2026_1SEM.xlsx` (executado, preenchimento manual irregular)
- Parser tolerante: tempos em formatos variados (ordinal, extenso, fração, intervalo)
- Cruza com `horarios_1semestre/grade_1semestre.py`
- Saída: `Relatorio_Tempos_Cedidos_1SEM.xlsx`

### analisar_2sem_2025.py 🟢

- Lê `provas2sem_2025/Klausurplan_ramoC_2025_2SEM.xlsx` (7 turmas, sem 12C2)
- `localizar()` reconstrói posição na grade (xlsx traz nº tempos, não quais)
- Saída: relatório de cessões 2025 para benchmark

### comparar_semestres.py 🟢

- Cruza `Relatorio_Tempos_Cedidos_1SEM.xlsx` vs `Relatorio_Tempos_Cedidos_Proposta_3.xlsx`
- Compara **percentual** (não absoluto — semestres têm durações diferentes)
- Saída: `Comparativo_Cessoes_1SEM_x_Proposta3.xlsx`

### Complexidade

**Média–alta** — parsers tolerantes para dados históricos irregulares.

---

## Feature: regras-negocio

**Arquivos:** `.claude/skills/calendario-provas/SKILL.md` (fonte viva, ~655 linhas), `exportar_regras_pdf.py`, `referencia/Regras_Negocio_Calendario_Provas.pdf`  
**Propósito:** Regras de negócio em linguagem humana; PDF é resumo para coordenação.

### Hierarquia de fontes 🟢

1. **SKILL.md** — verdade operacional (Passo 0, distribuição, cessão, entregáveis, checklist)
2. **Código** — `gerar_calendario.py`, `verificar_calendario.py`
3. **PDF** — gerado por `exportar_regras_pdf.py` (resumo estático; pode ficar atrás da skill)
4. **`referencia/estado_2sem_2026.md`** — dados concretos desta rodada

### Novidades na skill (sync 2026-08-09) 🟢

- Regra 4: afrouxamento só **depois** da prova; nunca antes/no dia
- `FORCAR_DATA` prioridade sobre coordenação de pares
- Seção "Regras relaxadas" obrigatória no relatório de trocas
- Checklist expandido: cores ARGB, amarelo simulados, mesclagem 3 linhas
- Orientação de semente e orçamento de nós (`MAX_NOS`)

### exportar_regras_pdf.py 🟡

- `build_pdf()` — resumo em 7 seções (não cobre todo o detalhe da skill)
- **Lacuna:** skill evolui mais rápido que o PDF — priorizar SKILL.md na fase Detetive/Writer

### Dependências

- `fpdf` (fpdf2)

### Complexidade

**Baixa** — geração estática de documento.

---

## Feature: plataforma-multi-coordenador (evolução futura)

**Arquivos:** nenhum código ainda — requisitos em `.reversa/context/user-requirements.md`  
**Propósito:** Plataforma web multi-usuário substituindo fluxo arquivo-local + git.

### Requisitos declarados 🟡

- 5 coordenadores, login individual, dados isolados por coordenador
- PostgreSQL (metadados) + blob storage (entradas/saídas)
- Backend Python FastAPI reaproveitando lógica de `gerar_calendario.py`
- Deploy híbrido: nuvem + Docker Compose on-prem

### Migração prevista 🟡

| Legado | Plataforma |
|---|---|
| `GRADES` hardcoded | Tabela `grade` por semestre/coordenador |
| Pastas `Horario desenvolvido/` | Blob + registro `CalendarioGerado` |
| `siglas/*.xlsx` | Upload versionado por coordenador |
| Scripts CLI | Endpoints API + fila de jobs |
| `verificar_calendario.py` | Validação pós-geração automática |

### Complexidade

**Alta** — nova arquitetura; detalhamento na fase **Arquiteto** (ERD, C4).
