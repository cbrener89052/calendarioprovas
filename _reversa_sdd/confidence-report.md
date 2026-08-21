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

## Lacunas críticas — resolvidas 🟡 (defaults 2026-08-21)

Ver ADR-014 e `_reversa_sdd/questions.md`. Resumo:

| ID | Status | Decisão |
|----|--------|---------|
| L-01 R-2CH | 🟡 | Must no forward (solver + verificador) |
| L-02 ENEM | 🟡 | Must no forward |
| L-03 Grade 2sem | 🟡 | Upload PDF plataforma; legado hardcode temporário |
| L-04 Auth | 🟡 | E-mail/senha + JWT + RLS |
| L-05 fpdf | 🟡 | Could legado; HTML regras plataforma v1 |

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

1. Priorizar implementação **R-2CH** no gerador antes do forward (skill já exige)
2. Validar **CalendarBlockPicker** e **ExamCatalogEditor** com coordenação (protótipo UX)
3. Golden file **Proposta_3** + grade PDF para testes de parser
4. Fechar decisão **auth** antes de `plataforma-multi-coordenador` T-02

---

## Histórico de Reclassificações

| De | Para | Afirmação | Evidência |
|----|------|-----------|-----------|
| 🟡 | 🟢 | Saída Excel obrigatória | ADR-013 + user-requirements |
| 🟡 | 🟢 | Bloqueios via UI visual | ADR-012 + user-requirements |
| 🟢 | 🟡 | Catálogo provas só xlsx | ADR-010 + ExamCatalogEditor |

---

## Próximo passo

- Brener pode **confirmar ou corrigir** defaults em `questions.md` (respostas 1b, 2a, 3b, 4a, 5b)
- `/reversa-forward` — prioridade: R-2CH/ENEM (L-01/L-02), auth T-02 (L-04)
- `/reversa-migrate` após primeira feature forward estável
- `/reversa-docs` — mini-site visual da documentação (opcional)
