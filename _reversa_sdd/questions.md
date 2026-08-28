# Perguntas para Validação — calendarioprovas

> **Status:** ✅ Todas respondidas — Brener 2026-08-21 / L-05 fechada 2026-08-28 (ADR-015)

---

## Pergunta 1 — L-01 R-2CH ✅

**Resposta:** **a** — Won't no código; checklist manual/skill.

---

## Pergunta 2 — L-02 ENEM ✅

**Resposta:** Custom — 2 datas ENEM + marcar disciplinas permitidas por janela de 6 dias.

Spec: `_reversa_sdd/ui/enem-week-config-spec.md`

---

## Pergunta 3 — L-03 Grade 2º sem ✅

**Resposta:** **b** — Upload PDF plataforma Must; legado `GRADE_TXT` até parser.

---

## Pergunta 4 — L-04 Auth ✅

**Resposta:** **c** — Conta compartilhada + PIN por coordenador (5 PINs).

---

## Pergunta 5 — L-05 fpdf ✅

**Resposta:** **d** — Regras **só na plataforma** (catálogo + Telas 1–2); **Won't** export PDF legado/fpdf na v1.

| Opção | Descrição |
|-------|-----------|
| a | Remover RF-05 |
| b | Could fpdf legado; HTML plataforma v1 |
| c | Must PDF plataforma v1 |
| **d** | **Regras na plataforma; Won't fpdf/PDF v1** |

---

## Resumo ADR-015

`1a, 2-custom, 3b, 4c, 5d`
