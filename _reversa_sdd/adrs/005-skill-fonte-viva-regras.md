# ADR-005 — Skill como fonte viva de regras

**Status:** Aceito (retroativo + evolução)  
**Data:** 2026-08-09 (`sources.json`, sync-regras)  
**Confiança:** 🟢

## Contexto

Regras existiam em três lugares: skill Markdown, constantes Python, checklist verificador — com risco de dessincronia (ex.: feriado 02/11).

## Decisão

- **Fonte viva principal:** `.claude/skills/calendario-provas/SKILL.md`
- Código = implementação; verificador = espelho
- Registrar fontes e hashes em `.reversa/context/sources.json`
- `_reversa_sdd/` = snapshot derivado (Detetive, Arqueólogo, Writer)

## Consequências

- ✅ Humanos editam regras em linguagem natural
- ⚠️ Duplicação BLOQUEIOS/FERIADOS persiste até refatoração
- ✅ Re-sync explícito após push GitHub

## Evidência Git

- Dezenas de commits `Skill: ...`
- `.reversa/context/sync-regras.md` (2026-08-15)
