# Relatório de Confiança — calendarioprovas

> Gerado pelo Revisor (Reversa) em 2026-08-21

---

## Resumo Geral

| Nível | Quantidade estimada | Percentual |
|-------|---------------------|------------|
| 🟢 CONFIRMADO | ~85 | ~62% |
| 🟡 INFERIDO | ~40 | ~29% |
| 🔴 LACUNA | ~12 | ~9% |
| **Total** | ~137 | 100% |

**Confiança geral:** ~82% — após resolução L-01–L-05 com defaults 🟡 (2026-08-21)

Legado Python + skill bem cobertos; plataforma alvo predominantemente 🟡.

---

## Por Unit

| Unit | 🟢 | 🟡 | 🔴 | Confiança |
|------|----|----|-----|-----------|
| `geracao-calendario/` | alto | médio | baixo | ~80% |
| `verificacao-calendario/` | alto | médio | médio | ~75% |
| `exportacao-relatorios/` | alto | médio | baixo | ~82% |
| `extracao-grade/` | alto | médio | alto (parser 2sem) | ~65% |
| `analise-historica/` | alto | alto | médio | ~70% |
| `regras-negocio/` | alto | médio | alto (2CH/ENEM) | ~68% |
| `plataforma-multi-coordenador/` | baixo | alto | médio | ~58% |

---

## Lacunas críticas — resolvidas 🟢 (Brener 2026-08-21, ADR-015)

| ID | Status | Decisão |
|----|--------|---------|
| L-01 R-2CH | 🟢 | **Won't** automatizar — manual/skill |
| L-02 ENEM | 🟢 | **Must** UI customizável (2 datas + disciplinas/janela) |
| L-03 Grade 2sem | 🟢 | Upload PDF plataforma; legado hardcode |
| L-04 Auth | 🟢 | Conta compartilhada + PIN |
| L-05 fpdf | 🔴 | Resposta "5d" — confirmar a/b/c |

### Pendentes moderadas 🟡

- DPA OpenAI + operação on-prem com API externa
- Framework frontend (Next.js provável)
- FERIADOS vs BLOQUEIOS unificação

---

## Inconsistências cruzadas (revisadas)

| Item | Status |
|------|--------|
| `FERIADOS` vs `BLOQUEIOS` | 🟡 ADR-012 propõe unificação — ainda no legado |
| Skill hash vs snapshot domain | 🟡 Re-rodar Detetive após sync skill recomendado |
| Máscara xlsx bloqueios vs CalendarBlockPicker | 🟢 ADR-012 resolve — xlsx secundário |

---

## Recomendações

1. Implementar **`EnemWeekConfigPanel`** + constraints solver (L-02)
2. Auth **conta + PIN** (L-04) antes de multi-coordenador T-02
3. Confirmar L-05 (export PDF regras)

---

## Histórico de Reclassificações

| De | Para | Afirmação | Evidência |
|----|------|-----------|-----------|
| 🟡 | 🟢 | Saída Excel obrigatória | ADR-013 + user-requirements |
| 🟡 | 🟢 | Bloqueios via UI visual | ADR-012 + user-requirements |
| 🟢 | 🟡 | Catálogo provas só xlsx | ADR-010 + ExamCatalogEditor |

---

## Próximo passo

- Brener confirmou **1a, 2-custom, 3b, 4c** — falta **5a/5b/5c** (informou "d")
- `/reversa-forward` — prioridade: ENEM config (L-02), auth PIN (L-04)
- `/reversa-migrate` após primeira feature forward estável
- `/reversa-docs` — mini-site visual da documentação (opcional)
