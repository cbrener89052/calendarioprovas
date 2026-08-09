# Relatório de Confiança — calendarioprovas

> Gerado pelo Revisor em 2026-08-09  
> Projeto: Escola Alemã Corcovado — calendário de provas  
> Usuário: Brener | doc_level: completo | layout: feature-folder

---

## Resumo Geral

| Nível | Quantidade | Percentual |
|-------|-----------|------------|
| 🟢 CONFIRMADO | 211 | 66,4% |
| 🟡 INFERIDO   | 71  | 22,3% |
| 🔴 LACUNA     | 36  | 11,3% |
| **Total**     | 318 | 100% |

**Confiança geral:** **77,5%** — fórmula: (🟢 + 🟡×0,5) / total

Interpretação: specs **aptas para reimplementação do CLI legado** com alta fidelidade; **plataforma multi-coordenador** requer validação das 4 perguntas em `questions.md` antes de codificar auth/IA/frontend.

---

## Por Feature

| Feature | 🟢 | 🟡 | 🔴 | Confiança |
|---------|----|----|-----|-----------|
| `geracao-calendario` | 52 | 12 | 10 | 78% |
| `verificacao-calendario` | 34 | 6 | 14 | 69% |
| `exportacao-relatorios` | 21 | 6 | 0 | 89% |
| `extracao-grade` | 24 | 7 | 1 | 86% |
| `analise-historica` | 15 | 5 | 0 | 88% |
| `regras-negocio` | 24 | 12 | 7 | 70% |
| `plataforma-multi-coordenador` | 41 | 23 | 4 | 77% |

**Melhor cobertura:** exportacao-relatorios, analise-historica (legado maduro).  
**Menor cobertura:** verificacao-calendario (lacunas PR #14 + ARGB + acoplamento).

---

## Lacunas Pendentes 🔴

Itens que permanecem sem confirmação após revisão — detalhes em `gaps.md`.

### geracao-calendario / verificacao-calendario / regras-negocio
- **LP/LIT/RED ≥10 dias antes conselho** — skill confirmada, código ausente (grep em `gerar_calendario.py` / `verificar_calendario.py`)
  - Pergunta: `questions.md#pergunta-4`

### regras-negocio / plataforma-multi-coordenador
- **Customização IA no pipeline** — ADR-006 🟢 declarado; ponto de integração 🔴
  - Pergunta: `questions.md#pergunta-2`

### plataforma-multi-coordenador
- **Admin institucional vs coordenador** — permissions 🟡
  - Pergunta: `questions.md#pergunta-1`
- **Frontend MVP** — stack não decidida
  - Pergunta: `questions.md#pergunta-3`

---

## Revisão Cruzada

- **Engine externa consultada:** Não (Codex indisponível nesta sessão)
- **Revisão interna:** 7 features, 22 arquivos canônicos + 3 globais
- **Apontamentos:** 3 correções aplicadas (MAX_NOS, OpenAPI, matrix)
- **Contradições críticas entre features:** 0

---

## Recomendações

- [ ] **Prioridade 1:** Responder `questions.md` (4 perguntas) antes de `/reversa-migrate` ou `/reversa-reconstructor`
- [ ] **Prioridade 2:** Implementar PR #14 no código (`T-06` geracao + `T-04` verificacao) — eleva confiança verificacao para ~85%
- [ ] **Prioridade 3:** Extrair módulo `rules/` compartilhado (gerador + verificador + RuleContext)
- [ ] **Prioridade 4:** Adicionar `requirements.txt` e smoke tests para 8 turmas seed 7
- [ ] Plataforma: MVP API-only reduz escopo se Pergunta 3 permitir

---

## Histórico de Reclassificações

| De | Para | Afirmação | Evidência |
|----|------|-----------|-----------|
| impreciso | 🟢 | MAX_NOS=60000, MAX_NOS_CESSAO=5000; ~600 nós/s é throughput com cessão | `gerar_calendario.py:657-664` |
| lacuna | corrigido | OpenAPI faltava `/customizacoes-ia` | Alinhado a `contracts.md` |
| n/a | 🟡 | `limpar_grade_2025.py`, `contar_2sem_2025.py` | `inventory.md` |

*Nenhum downgrade 🟢→🔴 necessário — afirmações confirmadas batem com código legado.*

---

## Veredicto Final

| Escopo | Confiança | Pronto para |
|--------|-----------|-------------|
| CLI legado (reimplementação) | **~85%** | `/reversa-reconstructor` com lacuna PR #14 documentada |
| Plataforma multi-coordenador | **~70%** | Design/spec OK; aguarda respostas RBAC + IA + frontend |
| Migração completa | **~75%** | `/reversa-migrate` após clarificar perguntas |

---

## Histórico

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | Relatório inicial Fase 5 | reversa-reviewer |
