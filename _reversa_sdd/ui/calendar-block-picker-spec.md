# Especificação UI — Calendário visual de bloqueios

> Componente: **`CalendarBlockPicker`**  
> Requisito usuário 2026-08-16 (4) | ADR-012  
> Confiança: 🟢 requisito | 🟡 detalhes visuais sujeitos a protótipo

## Propósito

Substituir planilhas Excel para feriados, semanas vetadas e dias sem prova.
O coordenador vê uma **malha de calendário** (semanas × seg–sex) e **clica**
para marcar onde **não pode haver prova**, por **turma** ou por **série**.

Persistência → `CalendarConstraints` → fatoração sem IA (ADR-011).

## Pré-requisitos (Must) 🟢

Antes da fatoração, o coordenador **Must** poder definir bloqueios via esta
tela (não via tabelas Excel):

1. **Grade horária** já carregada (define turmas e séries disponíveis).
2. **Período letivo** do semestre configurado (`SEMANA1`, última semana).
3. Acesso à tela **“Calendário — dias e semanas sem prova”**.

## Layout da tela

```
┌─────────────────────────────────────────────────────────────┐
│ Série: [9] [10] [11] [12]     Turma: [9C1 ▼]  (ou "Todas")   │
├─────────────────────────────────────────────────────────────┤
│        │ Seg │ Ter │ Qua │ Qui │ Sex │                        │
│ Sem 4  │ [ ] │ [ ] │ [ ] │ [ ] │ [X] │  ← clique semana = linha│
│ Sem 5  │ [ ] │ [■] │ [ ] │ [ ] │ [ ] │  ← clique dia = célula  │
│ ...    │     │     │     │     │     │                        │
├─────────────────────────────────────────────────────────────┤
│ Legenda: ■ sem prova  ◆ feriado  ★ simulado  · disponível    │
│ [Aplicar série → todas turmas]  [Limpar seleção]  [Salvar]   │
└─────────────────────────────────────────────────────────────┘
```

Malha visual alinhada ao **layout Klausurplan** (colunas E–I, semanas numeradas)
para reduzir carga cognitiva — não é o xlsx editável, é **espelho interativo**.

## Escopo de aplicação

| Modo | Seletor | Bloqueio afeta |
|------|---------|----------------|
| **Turma** | `10C1`, `10C2`, … | Só a turma escolhida |
| **Série** | `9`, `10`, `11`, `12` | Todas turmas da série (ex.: 10C1 + 10C2) |
| **Global** | opcional 🟡 | Feriados institucionais pré-carregados |

Requisito usuário: **por turma e por série** — ambos **Must**.

## Interações (Must)

| Gestão | Comportamento |
|--------|---------------|
| **Clique em dia** | Toggle `BlockedDay(turma\|série, semana, dia)` |
| **Clique em cabeçalho/semana** | Toggle `BlockedWeek(turma\|série, semana)` — todos os dias da semana |
| Semana bloqueada | Dias da semana aparecem bloqueados; clique em dia pode exceção 🟡 |
| Feriado institucional | Pré-marcado (ex.: 07/09); cor distinta; pode bloquear prova automaticamente |
| Simulado fixo | Marcador ★ — ocupa slot; editável em painel lateral 🟡 |

## Estados visuais das células

| Estado | Cor/ícone | Significado solver |
|--------|-----------|-------------------|
| Disponível | neutro | Provas móveis permitidas |
| Sem prova (coord.) | ■ vermelho/laranja | `dia_permitido` = false |
| Semana vetada | faixa na linha | `SEMANA_BLOQUEADA` equivalente |
| Feriado | ◆ cinza | Sem aula / sem prova |
| Simulado | ★ amarelo | `SIMULADOS` — data fixa |

## API (alvo) 🟡

| Método | Caminho | Descrição |
|--------|---------|-----------|
| GET | `/api/v1/calendars/{id}/constraints/grid` | Malha + bloqueios por `turma` ou `serie` |
| PUT | `/api/v1/calendars/{id}/constraints/day` | Toggle dia `{turma\|serie, w, d}` |
| PUT | `/api/v1/calendars/{id}/constraints/week` | Toggle semana `{turma\|serie, w}` |
| POST | `/api/v1/calendars/{id}/constraints/apply-serie` | Propaga bloqueio série → turmas |
| GET | `/api/v1/calendars/{id}/constraints/export` | xlsx backup (opcional) |

## Mapeamento → legado

| UI | Legado Python |
|----|---------------|
| Dia bloqueado | `BLOQUEIOS (w,d)` ou `OCUPADAS` |
| Semana bloqueada | `SEMANA_BLOQUEADA` |
| Feriado | `FERIADOS` + derivado `(w,d)` |
| Simulado | `SIMULADOS[turma]` |

## O que **não** é esta tela

- **Catálogo de provas** — ver `ExamCatalogEditor` / máscara provas (ADR-010).
- **Refração pós-geração** — grid de provas alocadas (`CalendarEditor`).
- **Planilha Excel de bloqueios** — export opcional; spec em
  `templates/mascara-bloqueios-calendario-spec.md` (secundário).

## Critérios de aceite

```gherkin
Cenário: Bloquear semana para série 10
  Dado coordenador na tela CalendarBlockPicker com série 10 selecionada
  Quando clica no cabeçalho da semana 11
  Então semanas 11 fica vetada para 10C1 e 10C2
  E CalendarConstraints persiste BlockedWeek para ambas turmas

Cenário: Bloquear terça de uma turma
  Dado turma 11C1 selecionada
  Quando clica terça da semana 5
  Então apenas 11C1 tem BlockedDay(5, 2)
  E 11C2 permanece disponível naquele dia

Cenário: Recálculo sem Excel e sem IA
  Dado bloqueios salvos via cliques na malha
  Quando coordenador dispara nova fatoração
  Então solver usa CalendarConstraints persistido
  E nenhuma chamada OpenAI ocorre na ingestão de bloqueios
```
