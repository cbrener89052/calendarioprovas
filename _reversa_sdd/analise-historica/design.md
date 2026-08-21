# Análise Histórica — Design

> Legado: `analisar_*.py`, `comparar_semestres.py`

## Scripts

| Script | Entrada | Métrica principal |
|--------|---------|-------------------|
| `analisar_1semestre` | xlsx 1º sem + GRADE_1SEM | Cessões por professor |
| `analisar_2sem_2025` | xlsx 2025 | Distribuição provas |
| `contar_2sem_2025` | xlsx 2025 | Soma tempos `(N)` |
| `comparar_semestres` | Dois xlsx | % cessão |

## Plataforma 🟡

- `HistoricalAnalysisService` — queries sobre `calendario` versionados
- `CalendarViewsService` — agregações JSON para copiloto (ADR-008)
- Opcional: materialized views PostgreSQL por semestre

## API (alvo)

| GET | `/api/v1/calendars/{id}/analytics/cessoes/compare?semestre_ref=` |

## Dependências

- openpyxl 🟢
- Proposta xlsx arquivados 🟢
- Exportação relatórios (mesmo parse) 🟡
