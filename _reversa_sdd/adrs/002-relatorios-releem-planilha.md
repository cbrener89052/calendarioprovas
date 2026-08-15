# ADR-002 — Relatórios derivados releem planilha gravada

**Status:** Aceito (retroativo)  
**Data:** 2026-08 (commits `#25`, `#26`, skill)  
**Confiança:** 🟢

## Contexto

Após refração manual, rodar `gerar_calendario.py` de novo **sobrescreve** o calendário com nova solução do solver, descartando edições humanas.

## Decisão

Scripts de exportação (`exportar_relatorio_trocas.py`, `exportar_tempos_cedidos.py`, etc.) **reconstroem** dados da planilha final via openpyxl — nunca da memória do backtracking.

Rotina obrigatória pós-edição manual: 5 scripts em ordem (skill, seção pós-edição).

## Consequências

- ✅ Relatórios fiéis ao que está na planilha entregue
- ✅ Seguro regenerar relatório sem tocar calendário
- ⚠️ Duplicação de lógica parse célula ↔ gerador

## Evidência Git

- `de6590c` / exportadores criados ou documentados em `#25`, `#26`
