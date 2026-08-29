# Exportação de Relatórios — Design Técnico

> Feature: `exportacao-relatorios` | Legado: `exportar_*.py`

## Interface

| Script | Entrada | Saída | Componente alvo |
|--------|---------|-------|-----------------|
| `exportar_tabelas_turma` | Proposta_3 xlsx | xlsx resumo/turma | `ReportExporter.tablesByClass` |
| `exportar_tempos_cedidos` | Proposta_3 xlsx | xlsx cessões agregadas | `ReportExporter.donatedTimes` |
| `exportar_relatorio_trocas` | Proposta_3 xlsx | md + xlsx 3 abas | `ReportExporter.tradeReport` |
| `exportar_provas_por_professor` | Proposta_3 xlsx | xlsx pivot professor | `ReportExporter.byTeacher` |
| ~~`exportar_regras_pdf`~~ (legado) | — | — | **Won't v1** — substituído por plataforma (ADR-015 5c) |
| — (plataforma) | catálogo + snapshot | PDF regras | `ReportExporter.rulesPdf` **Must** |

### API plataforma 🟡

| Método | Caminho | Saída |
|--------|---------|-------|
| POST | `/api/v1/calendars/{id}/exports` | job id |
| GET | `/api/v1/calendars/{id}/exports/{type}` | blob url |
| GET | `/api/v1/calendars/{id}/exports/rules/pdf` | PDF regras (Must v1) |
| GET | `/api/v1/calendars/{id}/exports/trades/preview` | JSON cessões (e-mail) |

## Fluxo Principal

1. Localizar `Proposta_3_*.xlsx` (path/blob) 🟢
2. `openpyxl.load_workbook(data_only=True)` 🟢
3. Parse células prova (mesma convenção verificador) 🟢
4. Agregar conforme script (turma / professor / doador) 🟢
5. Gravar xlsx/md/pdf de saída 🟢

**PDF regras (5c):** gerar a partir de `RulesCatalogService` + `RuleSetSnapshot` da rodada — não do script legado markdown estático.

**Princípio ADR-002:** pós-edição manual, coordenador reexecuta exports — skill seção pós-edição.

## Dependências

- openpyxl 🟢
- Proposta xlsx de `geracao-calendario` 🟢
- `verificacao-calendario` recomendado antes de fechar 🟡
- `DonorEmailService` consome trades 🟡
- `regras-negocio` — catálogo + snapshot para PDF 🟢 ADR-015
- Biblioteca PDF Python 🟡 (fpdf, WeasyPrint ou reportlab)

## Decisões

| Decisão | Evidência | Confiança |
|---------|-----------|-----------|
| Releitura xlsx | ADR-002 | 🟢 |
| Lógica duplicada entre scripts | architecture DT-07 | 🟢 |
| Trades = fonte e-mail | ADR-007 | 🟢 |
| PDF regras Must plataforma v1 | ADR-015 5c | 🟢 |

## Riscos

- 🟡 Drift parse export vs verificador
- 🟡 Paridade visual PDF plataforma vs `referencia/Regras_Negocio_*.pdf`
