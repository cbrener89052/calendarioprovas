# ADR-014 — Decisões das lacunas críticas da revisão

**Status:** Supersedido parcialmente por **ADR-015** (confirmação Brener 2026-08-21). Defaults abaixo válidos apenas onde ADR-015 não contradiz.
**Data:** 2026-08-21  
**Contexto:** Revisor identificou L-01–L-05 em `gaps.md`; usuário optou por continuar sem responder múltipla escolha.

## Decisão

| Lacuna | Decisão |
|--------|---------|
| **L-01 R-2CH** | Implementar no solver e verificador como regra **Must**; datas via UI/constraints (`"2CH <séries>"`). |
| **L-02 ENEM / véspera 9** | Implementar **Must**; véspera 2CH série 9 permanece **primeira flexível** da escada. |
| **L-03 Grade 2sem** | Plataforma: upload PDF Untis **Must**; legado mantém `GRADE_TXT` até parser dedicado. |
| **L-04 Auth** | E-mail + senha, JWT, isolamento row-level por coordenador; admin institucional separado. |
| **L-05 fpdf** | Legado: adicionar `fpdf` (Could); plataforma v1: regras em HTML/MD; PDF v1.1. |

## Consequências

- Forward prioriza T-12 R-2CH/ENEM em `geracao-calendario` antes de features cosméticas.
- `permissions.md` e `plataforma-multi-coordenador` deixam de bloquear T-02 com lacuna aberta.
- Confiança geral sobe ~76% → ~82% (lacunas críticas reclassificadas 🟡).

## Alternativas rejeitadas (por default)

- Won't em R-2CH/ENEM — conflita com skill viva pós-sync GitHub.
- SSO imediato — depende TI escola; adiado para v1.1+.
- Remover export PDF legado — mantém paridade referência `referencia/Regras_Negocio_*.pdf`.
