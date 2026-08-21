# ADR-015 — Lacunas confirmadas por Brener (2026-08-21)

**Status:** Aceito 🟢  
**Supersedes:** defaults 🟡 de ADR-014  
**Respostas:** `1a, 2-custom, 3b, 4c, 5-?`

## Decisões confirmadas

| ID | Resposta | Decisão |
|----|----------|---------|
| **L-01** | **a** | **Won't** automatizar R-2CH no solver/verificador — permanece skill + checklist manual/copiloto. |
| **L-02** | custom | **Must** UI `EnemWeekConfigPanel`: duas datas ENEM + disciplinas permitidas por janela (customizável). Spec: `_reversa_sdd/ui/enem-week-config-spec.md`. |
| **L-03** | **b** | Plataforma upload PDF Untis **Must**; legado `GRADE_TXT` até parser 2sem. |
| **L-04** | **c** | **Conta institucional compartilhada + PIN por coordenador** (5 PINs); auditoria por PIN. |
| **L-05** | **d** | 🔴 **Pendente** — opções eram apenas a/b/c; aguardar esclarecimento. |

## Consequências

- Forward **não** implementa T-12 R-2CH; implementa T-13 ENEM configurável.
- Auth: revisar decisão anterior "login individual e-mail/senha" → PIN sobre conta compartilhada.
- Skill continua fonte viva para R-2CH manual; produto não contradiz skill, adia automação.

## Histórico

| Data | Evento |
|------|--------|
| 2026-08-21 | Defaults ADR-014 (continuar sem respostas) |
| 2026-08-21 | Brener confirma 1a, 2-custom, 3b, 4c; L-05 aberta |
