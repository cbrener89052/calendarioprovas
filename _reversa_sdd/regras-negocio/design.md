# Regras de Negócio — Design

## Três camadas (ADR-005)

```
Skill Markdown (fonte viva)
    ↓ espelho
RulesCatalogService (BD + API)
    ↓ snapshot
RuleSetSnapshot → CalendarSolver / CalendarVerifier
    ↓ subset
Constantes gerar_calendario.py (legado)
```

## Componentes

| Componente | Papel |
|------------|-------|
| `RulesCatalogService` | CRUD catálogo; import skill; **substitui PDF regras** (ADR-015 5d) |
| `RulesSelectionWizard` | UI Telas 1–2 |
| `EnemWeekConfigPanel` | 2 datas ENEM + disciplinas/janela (ADR-015) |
| `RuleSetSnapshot` | JSON `{rule_id, aplicar, flexibilizar}` + `enem_week_config` |

## Sync fontes vivas

- `.reversa/context/sources.json` — hash SHA-256 skill
- Job opcional: diff skill → sugerir novas entradas catálogo 🟡

## API

| GET | `/api/v1/rules/catalog` |
| PUT | `/api/v1/calendars/{id}/rules/snapshot` |
| GET | `/api/v1/calendars/{id}/rules/snapshot` |
| PUT | `/api/v1/calendars/{id}/enem-config` |

## Lacunas código vs skill (pós ADR-015)

| Regra skill | Gerador legado | Plataforma alvo |
|-------------|----------------|-----------------|
| 2CH por período | 🔴 | **Won't v1** — manual |
| ENEM semanas | 🔴 | **Must** — `EnemWeekConfig` |
| Véspera 2CH 9C | 🔴 | **Won't v1** — manual |
| Fil/Soc exceção | 🟢 | 🟢 ADR-006 |

## Dependências

- Skill + `sources.json` 🟢
- `geracao-calendario`, `verificacao-calendario` 🟢
- `ui/enem-week-config-spec.md` 🟢
