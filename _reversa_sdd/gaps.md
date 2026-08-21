# Lacunas — calendarioprovas

> Gerado pelo Revisor | doc_level: completo  
> **Atualizado 2026-08-21:** L-01–L-05 resolvidas com defaults 🟡 (ver `questions.md`, ADR-014)

## Críticas 🔴

_Nenhuma lacuna crítica aberta — decisões registradas; implementação pendente no `/reversa-forward`._

## Resolvidas (defaults 🟡 — 2026-08-21)

| ID | Lacuna | Decisão | Unit |
|----|--------|---------|------|
| L-01 | R-2CH não implementada | **Must** implementar solver + verificador | regras-negocio / geracao |
| L-02 | ENEM / véspera 2CH | **Must** implementar; véspera 9 flexível primeiro | regras-negocio |
| L-03 | Parser grade 2º sem 2026 | Plataforma upload PDF Must; legado `GRADE_TXT` até parser | extracao-grade |
| L-04 | Auth/RBAC | E-mail + senha + JWT; RLS por coordenador | plataforma |
| L-05 | fpdf export regras | Could legado + HTML regras plataforma v1 | exportacao |

## Moderadas 🟡

| ID | Lacuna | Nota |
|----|--------|------|
| M-01 | FERIADOS vs BLOQUEIOS | CalendarConstraintsService |
| M-02 | Frontend stack | Next.js provável |
| M-03 | Merge catálogo upload + UI | ExamCatalog merge policy |
| M-04 | Skill → catálogo BD automático | RulesCatalogService import |
| M-05 | DPA OpenAI / on-prem | Migração / legal |
| M-06 | Portal professor read-only | Fora do escopo v1 |

## Cosméticas

- OpenAPI rascunho — expandir schemas na forward
- Duplicação parse xlsx exports (DT-07)
