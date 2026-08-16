# Dicionário de dados — calendarioprovas

> Gerado pelo Arqueólogo (Reversa) em 2026-08-15

## Entidades principais

### Grade horária (`GRADES` / `GRADE_TXT`)

| Campo | Tipo | Obrigatório | Descrição | Confiança |
|---|---|---|---|---|
| `turma` | `str` | sim | Código ex.: `10C1`, `11C2` | 🟢 |
| `dia` | `int` 1–5 | sim | Seg–Sex | 🟢 |
| `tempo` | `int` 1–11 | sim | Período do dia | 🟢 |
| `disc` | `str` | sim | Código abreviado (mat, DaF, plit, …) | 🟢 |
| `prof` | `str` | sim | Sigla(s); `/` ou `-` se múltiplos | 🟢 |

**Fonte:** `gerar_calendario.py` L80–250 (`GRADE_TXT` → `GRADES`).

### Exame / prova (lista de alocação)

| Campo | Tipo | Obrigatório | Descrição | Confiança |
|---|---|---|---|---|
| `disc` | `str` | sim | Disciplina ou `LPLITRED` combinada | 🟢 |
| `prof` | `str` | sim | Professor(es) | 🟢 |
| `n_tempos` | `int` | sim | 1, 2 ou 3 | 🟢 |
| `periodo` | `int\|None` | não | `1`, `2` ou `None` (prova única) | 🟢 |

**Fonte:** `montar_exames()` L577–609.

### Alocação resolvida (tupla canônica)

| Posição | Nome | Tipo | Descrição | Confiança |
|---|---|---|---|---|
| 0 | `w` | `int` | Número da semana letiva | 🟢 |
| 1 | `d` | `int` | Dia 1–5 | 🟢 |
| 2 | `t` | `int` | Tempo inicial | 🟢 |
| 3 | `n` | `int` | Duração em tempos | 🟢 |
| 4 | `disc` | `str` | Disciplina | 🟢 |
| 5 | `prof` | `str` | Professor(es) | 🟢 |
| 6 | `doador` | `tuple\|None` | `(disc, prof)` do tempo emprestado | 🟢 |

### Simulado (`SIMULADOS`)

| Campo | Tipo | Descrição | Confiança |
|---|---|---|---|
| chave | `(turma, codigo)` | ex.: `("10C1", "AG10")` | 🟢 |
| valor | `(semana, dia)` ou lista | Posição fixa no calendário | 🟢 |

### Célula ocupada (`OCUPADAS`)

| Campo | Tipo | Descrição | Confiança |
|---|---|---|---|
| chave | `turma` | Turma | 🟢 |
| valor | `set[(semana, dia)]` | Dias bloqueados no modelo | 🟢 |

### Sigla de professor

| Campo | Tipo | Fonte | Confiança |
|---|---|---|---|
| `sigla` | `str` | `siglas/siglas_profs_aux_etc.xlsx` | 🟢 |
| `nome` | `str` | mesma planilha | 🟢 |

### Relatório de cessão (exportação)

| Coluna | Tipo | Descrição | Confiança |
|---|---|---|---|
| Disciplina | `str` | Código | 🟢 |
| Professor | `str` | Sigla + nome | 🟢 |
| Nº aulas semanais | `int` | Contagem na grade | 🟢 |
| Nº aulas programadas | `int` | semanais × semanas letivas − feriados | 🟢 |
| Nº aulas cedidas | `int` | Tempos doados no semestre | 🟢 |
| % cedidas | `float` | cedidas / programadas | 🟢 |

### Perfil de regras (futuro — plataforma)

| Campo | Tipo | Descrição | Confiança |
|---|---|---|---|
| `rule_id` | `str` | ID no catálogo | 🟡 |
| `aplicar` | `bool` | Regra ativa na rodada | 🟡 |
| `flexibilizar` | `bool` | Pode relaxar no solver | 🟡 |

### Catálogo de provas — `ExamCatalog` (plataforma — ADR-010)

| Campo | Tipo | Obrigatório | Descrição | Confiança |
|---|---|---|---|---|
| `turma` | `str` | sim | Grupo/turma ex.: `10C1` | 🟢 |
| `disciplina` | `str` | sim | Nome ou código | 🟢 |
| `n_provas_semestre` | `int` | sim | Avaliações no semestre (1, 2, …) | 🟢 |
| `n_aulas_semanais` | `int` | sim | Tempos de aula/semana na grade (cessão C1) | 🟢 |
| `n_tempos` | `int` 1–3 | sim/não | Duração de cada prova; inferível | 🟢 |
| `periodo` | `int\|None` | não | 1ª/2ª ou única | 🟡 |
| `professor` | `str` | não | Sigla(s); default grade | 🟡 |
| `origem` | `enum` | sim | `mascara` \| `manual` \| `grade` \| `import` | 🟡 |
| `ordem` | `int` | não | Ordem da prova (1ª, 2ª) — aba `provas` | 🟢 |
| `escopo` | `enum` | sim | `fixa` \| `sessao` | 🟡 |
| `rodada_id` | `uuid` | não | Liga ao calendário gerado | 🟡 |

**Máscara provas:** `_reversa_sdd/templates/mascara-entrada-provas-spec.md`  
**Máscara bloqueios:** `_reversa_sdd/templates/mascara-bloqueios-calendario-spec.md`  
**Layout calendário:** `Klausurplan_2026_2SEM.xlsx` (GitHub) — não confundir.

**Fonte:** `.reversa/context/user-requirements.md` (2026-08-16).

### Restrições de calendário — `CalendarConstraints` (plataforma — ADR-011)

| Entidade | Campos principais | Origem máscara |
|---|---|---|
| `Holiday` | `data`, `descricao`, `tipo`, `escopo` | aba `feriados` |
| `BlockedWeek` | `semana`, `motivo`, `escopo` | aba `semanas_vetadas` |
| `BlockedDay` | `semana`, `dia`, `motivo`, `turmas[]` | aba `dias_bloqueados` |
| `FixedSimulado` | `turma`, `semana`, `dia`, `codigo`, `tempos` | aba `simulados` |
| `ForcedExamDate` | `turma`, `disciplina`, `periodo`, `semana`, `dia` | aba `datas_forcadas` |

Unifica legado `BLOQUEIOS`, `SEMANA_BLOQUEADA`, `SIMULADOS`, `FORCAR_DATA`, `FERIADOS`.

---

## Constantes de domínio (amostra)

| Constante | Tipo | Valores / papel | Arquivo |
|---|---|---|---|
| `SEM_PROVA` | `set[str]` | Disciplinas sem avaliação | gerar L200 |
| `GRUPO1` | `set[str]` | mat, DaF, port, LPLITRED, ing | gerar L394 |
| `BLOQUEIOS` | `set[(w,d)]` | Feriados por semana/dia | gerar L427 |
| `FERIADOS` | `set[date]` | Feriados por data | verificar L16 |
| `SEMANA_BLOQUEADA` | `set[int]` | Semana 11 (conselho) | gerar L433 |
| `TETO_PCT_CESSAO` | `float` | 0.11 (11%) | gerar L674 |
| `COORDENACAO_EXCECAO` | `set[tuple]` | Fil/Soc isentas regra 11 | verificar L44 |

---

## Arquivos de entrada/saída

| Caminho | Direção | Formato | Confiança |
|---|---|---|---|
| `Klausurplan_2026_2SEM.xlsx` | layout institucional | malha calendário (GitHub) | 🟢 |
| `Mascara_Entrada_Provas.xlsx` | entrada | catálogo + aba `provas` | 🟢 |
| `Mascara_Bloqueios_Calendario.xlsx` | entrada | feriados, bloqueios, simulados | 🟢 |
| `_reversa_sdd/templates/Mascara_Bloqueios_Calendario_2026_2SEM.xlsx` | exemplo | export legado 2º sem 2026 | 🟢 |
| `Horario desenvolvido/Proposta_3_*.xlsx` | saída | xlsx 8 abas | 🟢 |
| `Horario desenvolvido/Relatorio_trocas_de_tempo.md` | saída | markdown | 🟢 |
| `horarios turmas/*.pdf` | entrada | PDF Untis | 🟢 |
| `siglas/siglas_profs_aux_etc.xlsx` | entrada | xlsx | 🟢 |
