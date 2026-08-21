# Lacunas — calendarioprovas

> Atualizado 2026-08-21 — confirmado Brener (ADR-015)

## Críticas 🔴

| ID | Lacuna | Ação |
|----|--------|------|
| L-05 | `exportar_regras_pdf` / fpdf | Brener respondeu **5d** — opção inexistente; confirmar a/b/c |

## Resolvidas 🟢 (Brener 2026-08-21)

| ID | Lacuna | Decisão | Unit |
|----|--------|---------|------|
| L-01 | R-2CH | **Won't** automatizar — skill/checklist manual | regras-negocio |
| L-02 | ENEM | **Must** UI customizável (2 datas + disciplinas/janela) | regras-negocio / ui |
| L-03 | Grade 2º sem | Upload PDF plataforma Must; legado `GRADE_TXT` | extracao-grade |
| L-04 | Auth | Conta compartilhada + PIN por coordenador | plataforma |

## Moderadas 🟡

| ID | Lacuna | Nota |
|----|--------|------|
| M-01 | FERIADOS vs BLOQUEIOS | CalendarConstraintsService |
| M-02 | Frontend stack | Next.js provável |
| M-03 | Merge catálogo upload + UI | ExamCatalog merge policy |
| M-04 | Skill → catálogo BD automático | RulesCatalogService import |
| M-05 | DPA OpenAI / on-prem | Migração / legal |
| M-06 | véspera 2CH série 9 | Manual (alinhado a L-01 Won't) |

## Cosméticas

- OpenAPI rascunho — expandir schemas na forward
- Duplicação parse xlsx exports (DT-07)
