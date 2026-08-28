# ADR-015 — Lacunas confirmadas por Brener

**Status:** Aceito 🟢  
**Supersedes:** defaults 🟡 de ADR-014  
**Respostas finais:** `1a, 2-custom, 3b, 4c, 5d`

## Decisões confirmadas

| ID | Resposta | Decisão |
|----|----------|---------|
| **L-01** | **a** | **Won't** automatizar R-2CH no solver/verificador — skill + checklist manual/copiloto. |
| **L-02** | custom | **Must** UI `EnemWeekConfigPanel`: 2 datas ENEM + disciplinas permitidas/janela (customizável). Spec: `_reversa_sdd/ui/enem-week-config-spec.md`. |
| **L-03** | **b** | Plataforma upload PDF Untis **Must**; legado `GRADE_TXT` até parser 2sem. |
| **L-04** | **c** | **Conta institucional compartilhada + PIN** por coordenador (5 PINs); auditoria por PIN. |
| **L-05** | **d** | **Regras só na plataforma** — Won't `exportar_regras_pdf` / fpdf na v1; catálogo via `RulesCatalogService` + Telas 1–2; PDF export Could v2+. |

### Opção 5d (registrada em 2026-08-28)

Quarta opção implícita quando a/b/c não se aplicam:

- **Won't** manter script legado `exportar_regras_pdf.py` no escopo v1.
- **Won't** dependência `fpdf` no legado/plataforma v1.
- **Must** regras acessíveis na UI (catálogo + seleção Telas 1–2).
- Export PDF institucional — **Could** v2+ se coordenação solicitar.

## Consequências

- Forward **não** implementa T-12 R-2CH; implementa T-13 ENEM configurável.
- Auth: conta compartilhada + PIN (não e-mail/senha individual).
- Exportação-relatórios: RF-05 legado **Won't** v1; regras na feature `regras-negocio`.
- Skill continua fonte viva para R-2CH manual.

## Histórico

| Data | Evento |
|------|--------|
| 2026-08-21 | Defaults ADR-014 |
| 2026-08-21 | Brener confirma 1a, 2-custom, 3b, 4c |
| 2026-08-28 | L-05 fechada como **5d** — regras só plataforma |
