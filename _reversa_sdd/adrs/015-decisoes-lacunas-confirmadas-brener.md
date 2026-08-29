# ADR-015 — Lacunas confirmadas por Brener

**Status:** Aceito 🟢  
**Supersedes:** defaults 🟡 de ADR-014  
**Respostas finais:** `1a, 2-custom, 3b, 4c, 5c`

## Decisões confirmadas

| ID | Resposta | Decisão |
|----|----------|---------|
| **L-01** | **a** | **Won't** automatizar R-2CH no solver/verificador — skill + checklist manual/copiloto. |
| **L-02** | custom | **Must** UI `EnemWeekConfigPanel`: 2 datas ENEM + disciplinas permitidas/janela (customizável). |
| **L-03** | **b** | Plataforma upload PDF Untis **Must**; legado `GRADE_TXT` até parser 2sem. |
| **L-04** | **c** | **Conta institucional compartilhada + PIN** por coordenador (5 PINs); auditoria por PIN. |
| **L-05** | **c** | **Must** export **PDF institucional de regras na v1 da plataforma**; legado `exportar_regras_pdf.py` **Won't** v1. |

### Opção 5c (confirmada 2026-08-29)

- **Must** botão/download **PDF de regras** na plataforma (catálogo + snapshot da rodada).
- Gerado pelo backend (`ReportExporter.rulesPdf` ou equivalente) a partir de `RulesCatalogService` + `RuleSetSnapshot`.
- **Won't** manter script legado `exportar_regras_pdf.py` / `fpdf` no escopo v1 forward.
- Paridade de conteúdo com referência `referencia/Regras_Negocio_*.pdf` 🟡.

## Consequências

- Forward implementa **T-08** plataforma: PDF regras Must.
- Catálogo + Telas 1–2 continuam fonte; PDF é **export derivado**, não substituto da UI.
- Dependência PDF no backend (fpdf, WeasyPrint ou similar) — escolha na implementação 🟡.

## Histórico

| Data | Evento |
|------|--------|
| 2026-08-21 | Defaults ADR-014 |
| 2026-08-21 | Brener confirma 1a, 2-custom, 3b, 4c |
| 2026-08-28 | L-05 registrada como 5d (regras só plataforma) |
| 2026-08-29 | Brener corrige L-05 → **5c** (PDF Must plataforma v1) |
