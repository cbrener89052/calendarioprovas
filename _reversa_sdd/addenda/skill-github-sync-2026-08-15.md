# Adendo — sincronização skill GitHub (2026-08-15)

**Feature / evento:** sync fontes vivas após alterações no GitHub  
**Cenário:** legado  
**Vigente desde:** 2026-08-15.

## Resumo

O usuário pediu atualização com as skills do GitHub. Foi feito:

1. `git merge origin/main` — inclui PR #47 (ajustes 10C/12C em planilhas e `estado_2sem_2026.md`)
2. Hashes SHA-256 recalculados em `.reversa/context/sources.json`
3. Skill espelhada: `.agents/skills/calendario-provas/SKILL.md` ← `.claude/skills/...`
4. Fluxo documentado em `.reversa/context/sync-regras.md`

## Impacto por artefato

| Artefato | Seção | Tipo | Delta |
|---|---|---|---|
| `_reversa_sdd/code-analysis.md` | regras-negocio | delta-de-contrato | Fonte viva priorizada via `sources.json`; snapshot do Arqueólogo pode estar defasado |
| `_reversa_sdd/flowcharts/regras-negocio.md` | — | delta-de-contrato | Catálogo de regras = skill atual (1010 linhas), não só constantes Python |
| `referencia/estado_2sem_2026.md` | ajustes 10C/12C | delta-de-dados | Sincronizado com main (PR #47) |

## Regras sob vigilância

Nenhum watch item de ciclo forward ainda. Na fase Interpretação, o Detetive deve extrair regras da skill + código usando `sources.json`.

## Fontes

- `.claude/skills/calendario-provas/SKILL.md`
- `.reversa/context/sources.json`
- `.reversa/context/sync-regras.md`
