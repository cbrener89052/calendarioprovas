# ADR-004 — Skill como fonte viva de regras

**Status:** Aceito  
**Data:** 2026-08-09  
**Confiança:** 🟢

## Contexto

Regras evoluem via Claude Code (skill) mais rápido que código. Reversa precisava de sync explícito.

## Decisão

- `.claude/skills/calendario-provas/SKILL.md` = fonte humana principal
- `.reversa/context/sources.json` declara fontes canônicas + hashes
- Novas regras podem entrar só na skill primeiro (ex.: PR #14 LP/LIT/RED 10 dias)

## Consequências

- Lacunas documentadas quando skill > código
- Adendos em `_reversa_sdd/addenda/` até re-extração
- PDF (`exportar_regras_pdf.py`) é resumo estático, pode defasar
