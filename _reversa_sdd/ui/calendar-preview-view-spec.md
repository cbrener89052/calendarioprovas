# Especificação UI — Visualização do calendário (sem abrir Excel)

> Componente: **`CalendarPreviewView`**  
> Requisito usuário 2026-08-16 (5) | ADR-013  
> Confiança: 🟢 requisito | 🟡 detalhes visuais sujeitos a protótipo

## Propósito

Permitir que o coordenador **veja o calendário de provas gerado** (e, em
aba adjacente, a **grade horária** da turma) **dentro da plataforma**,
**sem abrir o Excel**. A **saída oficial** continua sendo o arquivo
`Proposta_3_<semestre>.xlsx` — a tela é **espelho read-only** do mesmo
conteúdo.

## Pré-requisitos (Must) 🟢

| # | Condição |
|---|----------|
| 1 | Fatoração concluiu e `Proposta_3_*.xlsx` foi gravado (blob + metadados) |
| 2 | Coordenador autenticado com acesso ao calendário da rodada |

## Saída Excel (Must) — inalterada

| Artefato | Formato | Ação na UI |
|----------|---------|------------|
| `Proposta_3_<semestre>.xlsx` | xlsx layout Klausurplan | **Baixar Excel** |
| `Relatorio_trocas_de_tempo.md` / xlsx | markdown / xlsx | Baixar relatório |
| Exports derivados | xlsx | Links na área de exportação |

A visualização **não substitui** o download; complementa.

## Layout — abas da tela

```
┌──────────────────────────────────────────────────────────────────┐
│ [Calendário de provas] [Grade horária]     Turma: [10C1 ▼]      │
│ [Baixar Excel]  [Verificar]  [Refração → CalendarEditor]         │
├──────────────────────────────────────────────────────────────────┤
│  Malha semanal (layout Klausurplan — read-only)                  │
│       Seg    Ter    Qua    Qui    Sex                            │
│  S4   Mat    ...   AG10   ...    ...                             │
│  S5   ...    ing   ...    LP/LIT ...                             │
│  ...                                                             │
├──────────────────────────────────────────────────────────────────┤
│ Legenda: prova · simulado · bloqueio · cessão (doador)           │
└──────────────────────────────────────────────────────────────────┘
```

### Aba 1: Calendário de provas (Must)

- Malha **idêntica** ao xlsx de saída (semanas × seg–sex, células com
  disciplina/professor/tempos).
- Seletor de **turma** (9C1 … 12C2) — equivalente às abas do Excel.
- **Somente leitura** nesta view; edição → `CalendarEditor`.
- Cores/alinhamento seguem convenções do Klausurplan legado 🟡.

### Aba 2: Grade horária (Should) 🟡

- Visualização da **grade semanal** carregada (slots de aula por dia/tempo).
- Ajuda o coordenador a cruzar provas alocadas × horário de classe **sem**
  abrir PDF/planilha externa.
- Fonte: parse da grade já ingerida (`GRADES` / blob grade).

## Dados e API (alvo) 🟡

| Método | Caminho | Descrição |
|--------|---------|-----------|
| GET | `/api/v1/calendars/{id}/preview/grid` | Malha Proposta_3 por `turma` |
| GET | `/api/v1/calendars/{id}/preview/timetable` | Grade horária por `turma` |
| GET | `/api/v1/calendars/{id}/download/xlsx` | Download `Proposta_3_*.xlsx` |

**Fonte de verdade:** blob xlsx gravado por `escrever()`. Preview = parse
do mesmo arquivo (paridade com verificador e exports).

## Atualização da view

| Evento | Comportamento |
|--------|---------------|
| Fatoração concluída | Preview disponível imediatamente |
| Refração / copiloto aceita alteração | Re-parse xlsx → refresh preview |
| Download Excel | Arquivo idêntico ao exibido na malha |

## Distinção de componentes UI

| Componente | Modo | Quando |
|------------|------|--------|
| `CalendarPreviewView` | Read-only | Revisar resultado; compartilhar tela |
| `CalendarEditor` | Edição | Refração manual pós-geração |
| `CalendarBlockPicker` | Edição bloqueios | **Antes** da fatoração |

## Critérios de aceite

```gherkin
Cenário: Visualizar calendário sem abrir Excel
  Dado Proposta_3 gerada para o semestre
  Quando o coordenador abre CalendarPreviewView e seleciona turma 10C1
  Então vê a malha semanal com as provas alocadas
  E o conteúdo corresponde à aba 10C1 do xlsx baixável

Cenário: Saída Excel preservada
  Dado calendário visualizado na plataforma
  Quando clica "Baixar Excel"
  Então recebe Proposta_3_<semestre>.xlsx no layout Klausurplan institucional

Cenário: Preview após refração
  Dado alteração aceita no CalendarEditor ou via copiloto
  Quando o xlsx é regravado
  Então CalendarPreviewView atualiza sem exigir download manual
```
