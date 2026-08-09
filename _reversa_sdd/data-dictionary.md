# Dicionário de dados — calendarioprovas

> Gerado pelo Arqueólogo (Reversa), doc_level=completo.

## Entidades principais (geracao-calendario)

### Turma 🟢

| Campo | Tipo | Exemplo | Descrição |
|---|---|---|---|
| codigo | string | `10C1` | Identificador da turma C |
| grupo | string | `10` | Grupo para fim de aulas / P2 |
| grade | map | `GRADES[codigo]` | `(dia, tempo) → (disc, prof)` |

### Exame (prova) 🟢

| Campo | Tipo | Descrição |
|---|---|---|
| disciplina | string | Código abreviado (`mat`, `LPLITRED`, …) |
| periodo | int | 1 ou 2 |
| n_tempos | int | 1, 2 ou 3 |
| rotulo | string | Texto na planilha (`LP/LIT/RED`, …) |

### Alocacao 🟢

| Campo | Tipo | Descrição |
|---|---|---|
| semana | int | Nº da semana no semestre (1–20) |
| dia | int | 1=Seg … 5=Sex |
| tempo_inicio | int | 1º tempo da prova |
| n_tempos | int | Duração |
| disciplina | string | Disciplina principal |
| doador | tuple | `(disc_doador, prof_doador)` se tempo emprestado |

### Cessao 🟢

| Campo | Tipo | Descrição |
|---|---|---|
| turma | string | Turma |
| chave | tuple | `(disciplina, professor)` doador |
| slot | tuple | `(semana, dia, tempo)` cedido |
| prova_beneficiaria | string | Disciplina que recebeu o tempo |

### Simulado 🟢

| Campo | Tipo | Descrição |
|---|---|---|
| codigo | string | `AG9`, `S3-11`, … |
| turmas | list | Turmas afetadas |
| semana | int | Semana fixa |
| dia(s) | int | Dia(s) da semana |
| tempos | range | Tipicamente 2–7 |

## Entidades futuras (plataforma-multi-coordenador) 🟡

| Entidade | Campos previstos |
|---|---|
| Coordenador | id, nome, email, instituição |
| Semestre | id, ano, periodo, coordenador_id |
| ArquivoEntrada | id, tipo (grade/modelo/simulados/siglas), path/blob, semestre_id |
| CalendarioGerado | id, proposta, semestre_id, xlsx_path, created_at |
| Relatorio | id, tipo (trocas/tabela/cessoes), calendario_id |

> Detalhamento ERD completo na fase do **Arquiteto**, após escavação.

---

## Entidades (verificacao-calendario)

### ProblemaValidacao 🟢

| Campo | Tipo | Descrição |
|---|---|---|
| turma | string | Ex.: `10C1` |
| proposta | int | 3 |
| regra | string | Identificador do check (1–11) |
| mensagem | string | Texto descritivo |
| severidade | enum | `problema` ou `aviso` |

### CelulaProva (parseada) 🟢

| Campo | Tipo | Descrição |
|---|---|---|
| data | date | Calculada de semana+dia |
| semana | int | 1–20 |
| dia | int | 1–5 |
| disciplina | string | 1ª linha da célula |
| t_ini | int | 1º tempo |
| n_tempos | int | Duração |
| destacada | bool | Cor ≠ preto (intervalo) |

---

## Entidades (exportacao-relatorios)

### SiglaProfessor 🟢

| Campo | Tipo | Descrição |
|---|---|---|
| sigla | string | Ex.: `BPad` |
| nome | string | Nome completo da planilha siglas |

### LinhaTabelaProvas 🟢

| Campo | Tipo | Descrição |
|---|---|---|
| disciplina | string | |
| professores | string | Siglas expandidas |
| quando | string | Dia, data, tempos |
| n_tempos | int | |

### LinhaCessao 🟢

| Campo | Tipo | Descrição |
|---|---|---|
| disciplina | string | Nome legível |
| professor | string | Sigla(s) |
| aulas_semanais | int | |
| aulas_programadas | int | Semestre inteiro |
| aulas_cedidas | int | Para provas de outras |
| percentual | float | cedidas / programadas |

---

## Entidades (extracao-grade)

### CelulaGrade 🟢

| Campo | Tipo | Descrição |
|---|---|---|
| turma | string | |
| dia | int | 1–5 |
| tempo | int | 1–11 |
| disciplina | string | |
| professor | string | Opcional (2025 OCR) |
| hora_inicio | string | 1sem 2026 only |

---

## Entidades (analise-historica)

### ComparativoCessao 🟢

| Campo | Tipo | Descrição |
|---|---|---|
| turma | string | |
| disciplina | string | |
| professor | string | |
| cedidas_1sem | int | |
| pct_1sem | float | |
| cedidas_p3 | int | |
| pct_p3 | float | |
| variacao_pp | float | Diferença percentual |
