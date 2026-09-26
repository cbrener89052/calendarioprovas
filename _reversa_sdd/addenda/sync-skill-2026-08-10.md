# Sync skill ↔ Reversa — 2026-08-10

> Disparado por: "SKILL ATUALIZADA, SINCRONIZE"  
> Merge: `origin/main` @ `5bcd2ae` (PR #18)

## Hashes atualizados

| Fonte | Hash anterior | Hash novo |
|-------|---------------|-----------|
| SKILL.md | `6be51fe2…` | `a010cbea…` |
| gerar_calendario.py | `c55c33c6…` | `9d8586c7…` |
| verificar_calendario.py | `0a554995…` | `a3c1e5b9…` |
| estado_2sem_2026.md | `d04c8838…` | `0b8563ac…` |

## Mudanças principais (PR #18)

### RN-08 LP/LIT/RED ≥10 dias — ✅ IMPLEMENTADO

| Componente | Detalhe |
|------------|---------|
| `gerar_calendario.py` | `LIMITE_LPLITRED_CONSELHO = 9`; `dia_permitido(..., disc)` vetora semanas >9 para LPLITRED |
| `verificar_calendario.py` | Check 5a-bis no checklist |
| SKILL.md | Regra + checklist; conflito potencial com 1ª/2ª semana rodada |

### Outras mudanças no gerador

| Mudança | Evidência |
|---------|-----------|
| `SEED_PROPOSTA_3 = 3` (era 7) | `gerar_calendario.py:678` — 10C1 com nova regra |
| `folga_extra` por turma | Escalonamento cessão localizado, não global |
| `resolver_par` → `falharam` | Falha coordenação professor comum não silenciosa |
| `detectar_regras_relaxadas` | Inclui regras 1 e 5 além de 3/4 |
| `posicoes_por_doador` | Corrige contagem em dobro de cessões (LP/LIT/RED 3 tempos) |
| Verificador regras 1/5 | AVISO quando relaxadas (como regra 4), não PROBLEMA |

### Resultado rodada

- 8 turmas fecham; **10C1** única com afrouxamento localizado (regra 3, 4, teto +1)
- `verificar_calendario.py`: OK, sem PROBLEMA
- Artefatos regerados em `Horario desenvolvido/`

### PDF

- `referencia/Regras_Negocio_Calendario_Provas.pdf` regerado via `exportar_regras_pdf.py`

## Módulos Reversa atualizados neste sync

- `regras-negocio`, `geracao-calendario`, `verificacao-calendario`
- `domain.md`, `code-analysis.md`, `modules.json`
- `gaps.md`, `confidence-report.md`, specs feature-folder
- `sources.json`

## Lacuna resolvida

- ~~G-C01 PR #14 código~~ → 🟢 implementado (#18)

## Reclassificações

| Item | De | Para |
|------|-----|------|
| RN-08 LP/LIT/RED 10 dias | 🔴 lacuna | 🟢 código + skill |
| SEED_PROPOSTA_3 | 🟢 = 7 | 🟢 = 3 |
| Escada folga cessão | 🟢 global | 🟢 global + folga_extra por turma |
