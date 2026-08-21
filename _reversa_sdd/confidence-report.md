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

**Confiança geral:** ~76% — `(62 + 29/2) ≈ 76%`

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

## Lacunas críticas 🔴

### Código vs skill
- **R-2CH (2ª chamada por período)** — skill 1051 linhas (sync 2026-08-20); gerador/verificador não implementam
- **ENEM / véspera 2CH** — documentado na skill; ausente no código
- **Parser grade 2º sem 2026** — `GRADE_TXT` hardcoded; plataforma depende de upload futuro

### Plataforma
- Auth provider e RBAC multi-coordenador não fechados
- DPA OpenAI + operação on-prem com API externa
- Framework frontend não decidido

### Infra
- `exportar_regras_pdf` — dependência `fpdf` ausente no cloud

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

- Responder lacunas 🔴 em chat ou `/reversa-clarify`
- `/reversa-forward` para implementação por feature
- `/reversa-migrate` após specs estáveis
