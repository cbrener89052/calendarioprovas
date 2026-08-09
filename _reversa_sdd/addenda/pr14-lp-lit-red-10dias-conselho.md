# Adendo — PR #14: LP/LIT/RED 10 dias antes do conselho

**Data:** 2026-08-09  
**Cenário:** legado  
**Fonte:** PR https://github.com/cbrener89052/calendarioprovas/pull/14 (branch `claude/skill-calendar-install-b2oqrs`)

## Vigência

Vigente desde 2026-08-09.

## Resumo

Nova regra documentada na skill (commit `8383e4d`): prova combinada **LP/LIT/RED** (3 tempos) deve ocorrer com **pelo menos 10 dias corridos** de antecedência do **início** da semana vetada de conselho de classe.

Exemplo: conselho começa 12/10/2026 → LP/LIT/RED não pode cair depois de 02/10/2026.

## Impacto por artefato

| Artefato | Tipo | Delta |
|---|---|---|
| `.claude/skills/calendario-provas/SKILL.md` | regra-nova | Seção distribuição + item checklist |
| `gerar_calendario.py` | lacuna | **Não implementado** (conforme PR #14) |
| `verificar_calendario.py` | lacuna | **Não implementado** |
| `_reversa_sdd/code-analysis.md` | regra-nova | Documentada com 🔴 lacuna |

## Conflito potencial

Skill avisa: pode conflitar com regra "1ª/2ª semana da rodada" — checar as duas juntas e avisar usuário se não houver semana válida.

## Fontes

- PR #14 diff
- `.claude/skills/calendario-provas/SKILL.md`
