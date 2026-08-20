# ADR-004 — Branches main vs producao

**Status:** Aceito (retroativo)  
**Data:** 2026-08 (`ae34182`, `referencia/fluxo-git-main-producao.md`)  
**Confiança:** 🟢

## Contexto

Desenvolvimento contínuo (skill, Reversa, rascunhos) misturava-se com versão entregue à escola.

## Decisão

| Branch | Papel |
|---|---|
| `main` | Desenvolvimento, propostas em elaboração, specs Reversa |
| `producao` | Snapshot validado após `verificar_calendario.py` OK |

Promoção via `promover_para_producao.bat` (merge main → producao).

## Consequências

- ✅ Escola consome branch estável
- ✅ Agentes cloud trabalham em `main` sem bloquear produção
- ⚠️ Risco de `main` divergir se promoção não for frequente

## Evidência Git

- `referencia/fluxo-git-main-producao.md`
- Commit `ae34182`
