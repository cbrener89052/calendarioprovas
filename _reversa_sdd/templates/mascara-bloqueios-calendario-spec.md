# Especificação — Máscara padrão de bloqueios e calendário letivo

> Template institucional para download/upload na plataforma  
> Requisito usuário 2026-08-16 (3) | ADR-011  
> Confiança: 🟢 requisito | 🟡 colunas finais sujeitas a validação com coordenação

## Propósito

Planilha **simples** que define **limites fixos** do semestre — dias de
recesso/feriado, semanas vetadas e dias em que **provas não podem ocorrer**
— sem depender do Klausurplan preenchido nem de interpretação por IA a cada
recálculo.

Fluxo:

1. **Baixa** — *"Baixe planilha de bloqueios e feriados"*
2. **Preenche** offline
3. **Upload** → `CalendarConstraints` (PostgreSQL) alimenta solver e verificador

Substitui, na plataforma, constantes hardcoded do legado (`BLOQUEIOS`,
`SEMANA_BLOQUEADA`, `SIMULADOS`, `FORCAR_DATA` parcial).

## Nome do arquivo (provisório)

`Mascara_Bloqueios_Calendario_<semestre>.xlsx`

## Aba 1: `feriados`

Dias **sem aula** (feriados nacionais, pontos facultativos, recesso escolar).

| Coluna | Cabeçalho PT | Tipo | Obrigatório | Descrição |
|--------|--------------|------|-------------|-----------|
| A | `data` | data ISO | sim | ex.: `2026-09-07` |
| B | `descricao` | texto | sim | ex.: Independência |
| C | `tipo` | enum | sim | `feriado` \| `recesso` \| `facultativo` |
| D | `escopo` | texto | não | vazio = todas turmas; ou `9,11` / `10,12` |

**Legado:** alimenta `FERIADOS` (verificador) e deriva `(semana, dia)` em `BLOQUEIOS`.

## Aba 2: `semanas_vetadas`

Semanas **inteiras** sem provas móveis (ex.: semana do conselho de classe).

| Coluna | Cabeçalho PT | Tipo | Obrigatório | Descrição |
|--------|--------------|------|-------------|-----------|
| A | `semana` | inteiro 1–20 | sim | Número da semana letiva |
| B | `motivo` | texto | sim | ex.: Conselho de classe |
| C | `escopo` | texto | não | vazio = global |

**Legado:** `SEMANA_BLOQUEADA`.

## Aba 3: `dias_bloqueados`

Dias específicos **sem prova** (distinto de feriado — ex.: evento escolar).

| Coluna | Cabeçalho PT | Tipo | Obrigatório | Descrição |
|--------|--------------|------|-------------|-----------|
| A | `semana` | inteiro | sim | Semana letiva |
| B | `dia` | 1–5 | sim | Seg=1 … Sex=5 |
| C | `motivo` | texto | sim | Motivo operacional |
| D | `turmas` | texto | não | vazio = todas; ou lista `10C1,10C2` |
| E | `bloqueia_prova` | S \| N | sim | Default `S` |

**Legado:** `BLOQUEIOS` + parte de `OCUPADAS` não-simulado.

## Aba 4: `simulados`

Datas **fixas** de simulados (ocupam slot; contam como avaliação/semana).

| Coluna | Cabeçalho PT | Tipo | Obrigatório | Descrição |
|--------|--------------|------|-------------|-----------|
| A | `turma` | texto | sim | ex.: `10C1` |
| B | `semana` | inteiro | sim | |
| C | `dia` | 1–5 | sim | |
| D | `codigo` | texto | sim | ex.: `AG10`, `S3-11` |
| E | `tempos` | texto | sim | ex.: `2º ao 7º tempos` ou `2-7` |
| F | `observacao` | texto | não | |

**Legado:** `SIMULADOS[turma]`.

## Aba 5: `datas_forcadas` (opcional)

Provas com data **obrigatória** (coordenação externa).

| Coluna | Cabeçalho PT | Tipo | Obrigatório | Descrição |
|--------|--------------|------|-------------|-----------|
| A | `turma` | texto | sim | |
| B | `disciplina` | texto | sim | |
| C | `periodo` | 1 \| 2 | sim | Qual prova |
| D | `semana` | inteiro | sim | |
| E | `dia` | 1–5 | sim | |
| F | `motivo` | texto | não | |

**Legado:** `FORCAR_DATA`.

## Validação no upload

| Regra | Severidade |
|-------|------------|
| `data`/`semana`/`dia` dentro do período letivo do semestre | PROBLEMA |
| Sem sobreposição ambígua feriado × dia_bloqueado (merge com AVISO) | AVISO |
| Simulado em dia bloqueado | PROBLEMA |
| Turma de simulado existe na grade | PROBLEMA |
| Sincronizar `feriados.data` → `(semana,dia)` coerente com `SEMANA1` | PROBLEMA |

## Mapeamento → `CalendarConstraints`

| Entidade | Origem abas |
|----------|-------------|
| `Holiday` | `feriados` |
| `BlockedWeek` | `semanas_vetadas` |
| `BlockedDay` | `dias_bloqueados` |
| `FixedSimulado` | `simulados` |
| `ForcedExamDate` | `datas_forcadas` |

Unificação **Must** gerador + verificador (resolve lacuna `FERIADOS` vs `BLOQUEIOS`).

## UI plataforma

- Botão **"Baixar planilha de bloqueios"** → xlsx com abas vazias + linhas exemplo do semestre anterior (se houver)
- Botão **"Enviar bloqueios preenchidos"** → parser → preview calendário → confirmar
- Alternativa: **`CalendarConstraintsEditor`** (mesmas colunas por aba)
- Recálculo/fatoração **Must** ler constraints persistidas — **sem** invocar copiloto

## Relação com IA (Must) 🟢

| Operação | Usa IA? |
|----------|---------|
| Upload máscara bloqueios → fatoração | **Não** |
| Upload máscara provas → fatoração | **Não** |
| Re-fatoração após editar máscaras | **Não** |
| Perguntas, diagnóstico, refração colaborativa | Sim (copiloto opcional) |

Objetivo do requisito: **limites já definidos nas máscaras** evitam consumo
de tokens OpenAI a cada recálculo de horário.

## Exemplo preenchido (2º sem 2026) 🟢

| Arquivo | Origem |
|---------|--------|
| `Mascara_Bloqueios_Calendario_2026_2SEM.xlsx` | Exportado de `gerar_calendario.py` + `verificar_calendario.py` |
| `gerar_mascara_bloqueios_exemplo.py` | Script regenerável na mesma pasta |

Conteúdo espelha o legado: 3 feriados, semana 11 vetada, 14 linhas de
simulados, 1 data forçada (Inglês 10C2). Aba `_meta` oculta com `SEMANA1`.
