# Especificação — Máscara padrão de entrada de provas

> Template institucional para download/upload na plataforma  
> Requisito usuário 2026-08-16 | ADR-010 (atualizado)  
> Confiança: 🟢 requisito | 🟡 colunas finais sujeitas a validação com coordenação

## Propósito

Arquivo xlsx **simples** (não é o Klausurplan semanal) que o coordenador:

1. **Baixa** na plataforma — *"Baixe sua planilha padrão aqui"*
2. **Preenche** offline com os dados pedidos
3. **Envia** de volta → sistema popula `ExamCatalog`

Distinto da **máscara de layout** Klausurplan (malha semanal de calendário).

## Nome do arquivo (provisório)

`Mascara_Entrada_Provas_<semestre>.xlsx`

## Visão geral das abas

| Aba | Conteúdo | Obrigatória no upload |
|-----|----------|------------------------|
| `catalogo` | Resumo por disciplina (carga + nº provas) | não — se `provas` completa |
| `provas` | **Uma linha por prova registrada** (ordem + tempos) | **sim** (preferencial) |

> Objetivo (ADR-011): dados tabulares determinísticos → recálculo **sem IA**.

## Aba: `catalogo` (resumo por disciplina)

| Coluna | Cabeçalho PT | Tipo | Obrigatório | Descrição |
|--------|--------------|------|-------------|-----------|
| A | `turma` | texto | sim | Grupo/turma ex.: `10C1` |
| B | `disciplina` | texto | sim | Nome ou código (Mat, Fil, LP/LIT/RED) |
| C | `n_provas_semestre` | inteiro 1–2 | sim | Quantidade de **provas** da disciplina no semestre |
| D | `n_aulas_semanais` | inteiro 0–11 | sim | **Tempos de aula por semana** na grade (carga semanal) |
| E | `n_tempos_aplicacao` | inteiro 1–3 | não | Default se todas provas iguais; senão usar aba `provas` |
| F | `periodo` | 1 \| 2 \| vazio | não | Só quando 1 prova com período explícito |
| G | `observacao` | texto | não | Notas livres (ignorado pelo solver) |

### Linhas de exemplo (pré-preenchidas no template, apagar antes de enviar)

```
10C1 | Mat | 2 | 4 | 2 | |
10C1 | LP/LIT/RED | 2 | 3 | 3 | |
10C1 | Fil | 1 | 1 | 1 | |
```

## Aba: `provas` — registro por prova (Must) 🟢

Tabela no **formato de ordem**: cada linha = **uma prova** a fatorar.

| Coluna | Cabeçalho PT | Tipo | Obrigatório | Descrição |
|--------|--------------|------|-------------|-----------|
| A | `turma` | texto | sim | ex.: `10C1` |
| B | `disciplina` | texto | sim | Mat, LP/LIT/RED, Fil, … |
| C | `ordem_prova` | inteiro 1–2 | sim | **Ordem** da prova no semestre (1ª, 2ª) |
| D | `n_tempos_aplicacao` | inteiro 1–3 | sim | **Tempos de aula** que a prova ocupa |
| E | `n_aulas_semanais` | inteiro 0–11 | sim | Carga semanal da disciplina (cessão C1) |
| F | `periodo` | 1 \| 2 | não | Alias de `ordem_prova` quando skill exige período |
| G | `professor` | texto | não | Sigla(s); default = grade |
| H | `observacao` | texto | não | Ignorado pelo solver |

### Exemplo (Mat 2 provas, LP/LIT/RED 2 provas de 3 tempos)

```
10C1 | Mat | 1 | 2 | 4 | 1 |
10C1 | Mat | 2 | 2 | 4 | 2 |
10C1 | LP/LIT/RED | 1 | 3 | 3 | 1 |
10C1 | LP/LIT/RED | 2 | 3 | 3 | 2 |
10C1 | Fil | 1 | 1 | 1 | |
```

### Regras de consistência entre abas

| Regra | Severidade |
|-------|------------|
| Contagem de linhas `(turma, disciplina)` em `provas` = `n_provas_semestre` em `catalogo` | AVISO se só uma aba; PROBLEMA se conflito |
| `ordem_prova` sequencial 1..N sem buracos | PROBLEMA |
| `n_aulas_semanais` igual em todas linhas da mesma `(turma, disciplina)` | PROBLEMA |

## Validação no upload

| Regra | Severidade |
|-------|------------|
| Aba `provas` presente e não vazia (preferencial) | AVISO se só `catalogo` |
| Turma existe na grade carregada | PROBLEMA se ausente |
| Disciplina existe na turma (grade) | AVISO se divergir |
| `n_provas_semestre` coerente com skill (ex.: Fil=1) | PROBLEMA |
| `n_aulas_semanais` coerente com `aulas_semanais(turma)` | AVISO |
| LP/LIT/RED com `n_tempos_aplicacao`=3 (10–12) | PROBLEMA |
| `ordem_prova` única por `(turma, disciplina)` | PROBLEMA |

## Mapeamento → `ExamCatalog`

**Preferencial:** cada linha da aba `provas` → um exame:

- `n_tempos` ← coluna D
- `periodo` ← coluna F ou C (`ordem_prova`)
- `n_aulas_semanais` ← coluna E
- `ordem` ← coluna C (metadado UI)

**Fallback:** aba `catalogo` expande `n_provas_semestre` em N linhas com
`n_tempos` da coluna E ou inferido pela skill.

## UI plataforma

- Botão **"Baixar planilha padrão de provas"** → xlsx com abas `catalogo` + `provas` (cabeçalhos + exemplos)
- Botão **"Enviar planilha preenchida"** → parser → preview → confirmar
- Alternativa: **`ExamCatalogEditor`** — grid espelhando aba `provas` (ordem + tempos por linha)
- Recálculo consome `ExamCatalog` persistido — **sem** copiloto na ingestão (ADR-011)

## Referência legado (layout calendário — outro arquivo)

| Arquivo GitHub | Papel |
|----------------|-------|
| `Klausurplan_2026_2SEM.xlsx` | **Layout** malha semanal 2º sem 2026 |
| `Horario modelo/Klausurplan_2026_1SEM.xlsx` | Layout 1º sem |
| `provas2sem_2025/Klausurplan_ramoC_2025_2SEM.xlsx` | Layout referência 2025 |
| `Horario desenvolvido/Proposta_3_*.xlsx` | Saída gerada (usa layout) |
