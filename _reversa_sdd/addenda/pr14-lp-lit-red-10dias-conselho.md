# Adendo — PR #14: LP/LIT/RED 10 dias antes do conselho

**Data:** 2026-08-09 (skill) / **2026-08-10** (código PR #18)  
**Status:** ✅ **Implementado**

## Vigência

- Skill: PR #14 mergeada em `main`
- Código: PR #18 (`5bcd2ae`)

## Implementação

| Arquivo | Mecanismo |
|---------|-----------|
| `gerar_calendario.py` | `LIMITE_LPLITRED_CONSELHO = 9`; `dia_permitido(w, disc)` |
| `verificar_calendario.py` | Checklist 5a-bis |

## Mudanças correlatas (PR #18)

- `SEED_PROPOSTA_3 = 3`
- `folga_extra` por turma
- Regras 1/5 → AVISO no verificador quando relaxadas
- `posicoes_por_doador` — fix contagem cessão

Ver `_reversa_sdd/addenda/sync-skill-2026-08-10.md`.
