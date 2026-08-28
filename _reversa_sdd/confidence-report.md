# Relatório de Confiança — calendarioprovas

> Gerado pelo Revisor (Reversa) | Atualizado 2026-08-28 (ADR-015 completo)

---

## Resumo Geral

| Nível | Quantidade estimada | Percentual |
|-------|---------------------|------------|
| 🟢 CONFIRMADO | ~92 | ~67% |
| 🟡 INFERIDO | ~38 | ~28% |
| 🔴 LACUNA | ~7 | ~5% |
| **Total** | ~137 | 100% |

**Confiança geral:** ~86% — lacunas críticas L-01–L-05 fechadas (ADR-015)

---

## Por Unit

| Unit | Confiança |
|------|-----------|
| `geracao-calendario/` | ~82% |
| `verificacao-calendario/` | ~78% |
| `exportacao-relatorios/` | ~85% |
| `extracao-grade/` | ~72% |
| `analise-historica/` | ~70% |
| `regras-negocio/` | ~80% |
| `plataforma-multi-coordenador/` | ~68% |

---

## Lacunas críticas — todas resolvidas 🟢 (ADR-015)

| ID | Decisão |
|----|---------|
| L-01 R-2CH | **Won't** automatizar — manual/skill |
| L-02 ENEM | **Must** UI customizável |
| L-03 Grade 2sem | Upload PDF plataforma |
| L-04 Auth | Conta + PIN |
| L-05 fpdf | **Won't v1** — regras só plataforma (5d) |

### Moderadas restantes 🟡

- FERIADOS vs BLOQUEIOS
- Frontend Next.js
- DPA OpenAI / on-prem
- Perfil regras por coordenador vs semestre

---

## Recomendações forward

1. `EnemWeekConfigPanel` + T-13 solver/verificador
2. Auth conta + PIN (T-02)
3. `GradeParserService` upload PDF (T-05 plataforma)

---

## Próximo passo

- **`/reversa-forward`** — implementação por feature
- **`/reversa-migrate`** — specs sistema novo
- **`/reversa-docs`** — mini-site (opcional)
