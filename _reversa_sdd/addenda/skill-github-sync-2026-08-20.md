# Adendo — sincronização skill GitHub (2026-08-20)

**Feature / evento:** sync fontes vivas com `origin/claude/skill-calendar-install-b2oqrs`  
**Cenário:** legado + branch Reversa  
**Vigente desde:** 2026-08-20.

## Resumo

Pedido do usuário: alinhar local e skills ao GitHub.

1. `git merge origin/claude/skill-calendar-install-b2oqrs` (239b703)
2. Skill `.claude/skills/calendario-provas/SKILL.md` — restauradas regras 2ª chamada (2CH) e Passo 0 item 14
3. Espelho `.agents/skills/calendario-provas/SKILL.md` ← cópia idêntica (Cursor)
4. Hashes em `.reversa/context/sources.json` recalculados
5. Atualizados: `referencia/estado_2sem_2026.md`, `Horario desenvolvido/*`, `professores_comuns_reuniao_C_2026.xlsx`

## Localização das skills (inalterada)

| Papel | Caminho Claude Code | Espelho Cursor |
|-------|---------------------|----------------|
| Regras calendário | `.claude/skills/calendario-provas/SKILL.md` | `.agents/skills/calendario-provas/SKILL.md` |
| Orquestrador Reversa | `.claude/skills/reversa/SKILL.md` | `.agents/skills/reversa/SKILL.md` |

Ver `.reversa/context/sync-regras.md` e `sources.json`.

## Impacto Reversa

| Artefato | Ação sugerida |
|---|---|
| `_reversa_sdd/domain.md` | Revisar regras 2CH se Detetive re-rodar |
| `regras-negocio` (Writer pendente) | Extrair novas regras da skill (1051 linhas) |
| `geracao-calendario` | Lacuna 2CH ainda no gerador — skill documenta, código não |

## Fontes

- `.reversa/context/sources.json` — hash `b2431d19…` da skill
- Commit base GitHub: `239b703`
