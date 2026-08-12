# Addendum — GitHub como fonte da verdade (2026-08-12)

**Confiança:** 🟢 (decisão operacional confirmada por Brener)  
**Escopo:** skill, sync Reversa, documentação, agentes cloud

## Decisão

O repositório remoto **GitHub** (`origin/main`) é a **fonte da verdade** para:

- Regras de negócio (`.claude/skills/calendario-provas/SKILL.md`)
- Implementação (`gerar_calendario.py`, `verificar_calendario.py`, exportadores)
- Referência da rodada (`referencia/`)
- Specs Reversa versionadas (`_reversa_sdd/`, `.reversa/`)

Cópias locais (Windows, VM do agente) são **rascunhos até push**. `_reversa_sdd/` é **derivado** — útil para migração, mas não substitui o remoto.

## Artefatos atualizados

| Arquivo | Alteração |
|---|---|
| `.claude/skills/calendario-provas/SKILL.md` | Seção "Fonte da verdade — GitHub" |
| `.reversa/context/sync-regras.md` | Hierarquia com GitHub prioridade 0 |
| `.reversa/context/sources.json` | Metadados `github_repo`, branches |
| `_reversa_sdd/adrs/004-skill-fonte-viva-regras.md` | ADR ampliado |
| `README.md`, `referencia/fluxo-git-main-producao.md` | Fluxo explícito |

## Implicações para a plataforma (migração)

| Legado | Plataforma |
|---|---|
| Git + pastas locais | PostgreSQL + blobs por coordenador |
| Skill no repo | Seed `regra_catalogo` a partir de GitHub |
| `main` / `producao` | Deploy preview vs produção (paridade conceitual) |

O catálogo no BD é **operacional**; alterações institucionais de regra continuam originando no GitHub (skill + PR) até processo de sync formal existir na UI admin.

## RN-01 refinado

**RN-01 (atualizado):** A fonte de verdade das regras de domínio é a skill em **GitHub `main`**; PDF e `_reversa_sdd/` são derivados.
