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
| `RulesCatalogService` | CRUD catálogo; import skill |
| `RulesSelectionWizard` | UI Telas 1–2 |
| `RuleSetSnapshot` | JSON `{rule_id, aplicar, flexibilizar}` |

## Sync fontes vivas

- `.reversa/context/sources.json` — hash SHA-256 skill
- Job opcional: diff skill → sugerir novas entradas catálogo 🟡

## API

| GET | `/api/v1/rules/catalog` |
| PUT | `/api/v1/calendars/{id}/rules/snapshot` |
| GET | `/api/v1/calendars/{id}/rules/snapshot` |

## Lacunas código vs skill

| Regra skill | Gerador | Verificador |
|-------------|---------|-------------|
| 2CH por período | 🔴 | 🔴 |
| ENEM semana anterior | 🔴 | 🟡 doc |
| Fil/Soc exceção | 🟢 | 🟢 ADR-006 |

## Dependências

- Skill + `sources.json` 🟢
- `geracao-calendario`, `verificacao-calendario` 🟢
