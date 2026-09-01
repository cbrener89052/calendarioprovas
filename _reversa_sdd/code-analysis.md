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

Implementa regras 1–5 de cessão de aula:
- Tetos por `(disciplina, professor)` por turma
- Regra 3: duas semanas seguidas sem contato
- Regra 4: não ceder na semana da prova nem na anterior
- Regra 5: teto percentual 11% das aulas programadas
- Métodos: `pode_ceder_bloco`, `pode_alocar_exame`, `aplicar`, `desfazer`, `clone`

### Regras embutidas no código 🟢

- Máx. 3 avaliações/semana; 1 prova/dia
- Grupo 1 (Mat, DaF, Port/LPLITRED, Ing) não coincide (exceção: 2 com Ing)
- Distância mínima 4 semanas entre provas da mesma disciplina
- Não cruzar intervalo 3+4 / 5+6 tempos (prioridade máxima)
- LP/LIT/RED turmas 10–12: 3 tempos, semanas 1–2 de cada rodada
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

| # | Regra | Tipo |
|---|---|---|
| 1 | Máx. 3 avaliações/semana (simulado 2 dias = 1) | problema |
| 2 | Grupo 1 não coincide (exc. 2 com Ing) | problema |
| 3 | Uma prova por dia | problema |
| 4 | Datas dentro do período, sem feriado/semana vetada | problema |
| 5 | Nº provas por disciplina; LP/LIT/RED separado; distância mínima 4 sem | problema |
| 5b | LP/LIT/RED com 3 tempos (10–12) | problema |
| 5c | Simulados 2º–7º tempo | problema |
| 6 | Disciplinas 1 tempo usam 1 tempo | problema |
| 7 | Sem prova de Ed.Física, Artes, etc. | problema |
| 7b | Provas 7–11 só se inevitável (opcional manhã) | aviso (P3) |
| 7c | Disciplina 1 aula/semana não cede tempo | problema |
| 8 | Simulados nas datas oficiais (`G.SIMULADOS`) | problema |
| 9 | Não cruzar intervalo sem destaque laranja | problema |
| 10 | Datas em `G.FORCAR_DATA` | problema |
| 10b | Limites cessão regras 1–5 (Proposta 3) | problema/aviso |
| 11 | Provas professor comum em turmas irmãs coincidem | problema |

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

**Arquivos:** `exportar_regras_pdf.py`, `.claude/skills/calendario-provas/SKILL.md`, `referencia/Regras_Negocio_Calendario_Provas.pdf`  
**Propósito:** Documentar regras de negócio em PDF legível para coordenação.

### exportar_regras_pdf.py 🟢

- `build_pdf()` — gera PDF com fpdf2 (fonte DejaVu)
- Seções: entradas, períodos/bloqueios, distribuição, cessão P3, simulados, formato saída, entregáveis
- Conteúdo espelha a skill `calendario-provas` (fonte de verdade humana)
- Saída: `referencia/Regras_Negocio_Calendario_Provas.pdf`

### Relação código ↔ regras 🟢

| Regra documentada | Implementação |
|---|---|
| Backtracking + cessão | `gerar_calendario.py:Cessoes` |
| Checklist 11 itens | `verificar_calendario.py:main` |
| Limites percentuais | `G.TETO_PCT_CESSAO`, `programadas_no_semestre` |

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
