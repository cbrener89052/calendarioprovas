# Lacunas — calendarioprovas

> Atualizado 2026-08-28 — **todas as lacunas críticas L-01–L-05 fechadas** (ADR-015)

## Críticas 🔴

_Nenhuma._

## Resolvidas 🟢 (ADR-015)

| ID | Lacuna | Decisão | Unit |
|----|--------|---------|------|
| L-01 | R-2CH | **Won't** automatizar — skill/checklist manual | regras-negocio |
| L-02 | ENEM | **Must** UI customizável (2 datas + disciplinas/janela) | regras-negocio / ui |
| L-03 | Grade 2º sem | Upload PDF plataforma Must; legado `GRADE_TXT` | extracao-grade |
| L-04 | Auth | Conta compartilhada + PIN por coordenador | plataforma |
| L-05 | fpdf / PDF regras | **Won't** v1 — regras só na plataforma; PDF Could v2+ | regras-negocio / exportacao |

## Moderadas 🟡

| ID | Lacuna | Nota |
|----|--------|------|
| M-01 | FERIADOS vs BLOQUEIOS | CalendarConstraintsService |
| M-02 | Frontend stack | Next.js provável |
| M-03 | Merge catálogo upload + UI | ExamCatalog merge policy |
| M-04 | Skill → catálogo BD automático | RulesCatalogService import |
| M-05 | DPA OpenAI / on-prem | Migração / legal |
| M-06 | véspera 2CH série 9 | Manual (alinhado L-01 Won't) |
| M-07 | Perfil regras por coordenador vs semestre | user-requirements pendente |
| M-08 | Export PDF regras v2+ | Could pós-v1 se escola solicitar |

## Cosméticas

- OpenAPI rascunho — expandir schemas na forward
- Duplicação parse xlsx exports (DT-07)
