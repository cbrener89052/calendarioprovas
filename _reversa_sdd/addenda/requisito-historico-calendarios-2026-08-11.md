# Addenda — Histórico de calendários gerados (2026-08-11)

> Pedido de Brener via `/reversa` — requisito declarado em `.reversa/context/user-requirements.md`

## Resumo

Cada geração de calendário deve ser **persistida automaticamente** (BD + blobs). O coordenador gerencia versões pela UI: consultar, baixar, restaurar referência e apagar.

## Artefatos atualizados

| Artefato | Alteração |
|----------|-----------|
| ADR-009 | Decisão arquitetural versionamento INSERT-only |
| `plataforma-multi-coordenador/requirements.md` | RF-15–RF-18, RN-09–RN-10 |
| `plataforma-multi-coordenador/design.md` | Fluxo + endpoints histórico |
| `plataforma-multi-coordenador/tasks.md` | T-10b, T-10c, TT-05 |
| `plataforma-multi-coordenador/contracts.md` | API histórico |
| `openapi/calendarioprovas.yaml` | Paths + schema `CalendarioVersao` |
| `migration/target_screens.md` | SCR-10 |
| `erd-complete.md` | Colunas `versao`, `rotulo`, `referencia_ativa`, `deleted_at` |
| `user-stories/fluxo-calendario-semestre.md` | US-08 |

## Implementação (reconstruction-plan)

- Worker/API: estender T6/T10 — INSERT-only em `calendario_gerado`
- Frontend: T13 — SCR-10 Histórico
- Migration futura: colunas ADR-009 em `calendario_gerado`

## Confiança

🟢 — requisito explícito do usuário; sem ambiguidade de escopo.
