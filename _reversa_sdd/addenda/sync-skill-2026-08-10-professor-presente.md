# Sync Reversa — regra prioridade 1 professor presente (2026-08-10)

> Merge base `claude/skill-calendar-install-b2oqrs` @ 677cec0 into `cursor/reversa-reconstruct-b8d6`

## Commit incorporado

| SHA | Conteúdo |
|-----|----------|
| 677cec0 | Regra prioridade 1: professor presente na aplicação da prova |

## Alterações de código

| Arquivo | Mudança |
|---------|---------|
| `gerar_calendario.py` | `professor_presente_no_bloco()`; checagem em `_tentar_par` e alocação; import `re` |
| `verificar_calendario.py` | Checklist espelha presença do professor no bloco |
| `SKILL.md` | Seção PRIORIDADE 1 — presença na aplicação; checklist atualizado |
| `referencia/estado_2sem_2026.md` | Documentação da regra e correções manuais Proposta 3 |
| xlsx Proposta 3 | Regenerados |

## Impacto plataforma / Reversa

- **Seed catálogo**: nova regra `professor_presente_aplicacao_prova` (39 entradas)
- **Solver T5**: extrair `professor_presente_no_bloco` para `packages/solver`
- **Parity test**: TT presença professor no bloco (verificador)

## Hashes

Ver `.reversa/context/sources.json` — sync pós 677cec0.
