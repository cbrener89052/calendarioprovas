---
schemaVersion: 1
generatedAt: 2026-08-10T02:25:00Z
reversa:
  version: "1.2.58"
kind: ambiguity_log
producedBy: orchestrator
---

# Ambiguity Log — Migração calendarioprovas

## PENDENTES

(nenhum — pipeline migrate concluído)

## RESOLVIDOS COM DECISÃO HUMANA

| ID | Item | Resolução | Decisor | Data |
|----|------|-----------|---------|------|
| AMB-001 | RBAC admin vs coord | Brener admin_instituicao; coords isolados | Brener | 2026-08-09 |
| AMB-002 | Escopo IA | Verificador + relatório auxiliar | Brener | 2026-08-09 |
| AMB-003 | Frontend v1 | React Vite + Tailwind | Brener | 2026-08-09 |
| AMB-004 | PR #14 Must | Implementado PR #18 | Brener/sync | 2026-08-10 |

## REFERIDOS À CODIFICAÇÃO

| ID | Item | Onde decidir | Nota |
|----|------|--------------|------|
| AMB-C01 | Context vs Redux | T-13 plataforma | auto: implementador escolhe |
| AMB-C02 | Validação ARGB cores | verificador plataforma | MIGRAR Should (BR-MIGRAR-031) |
| AMB-C03 | Audit log toggles | API regras | Should v1 |
| AMB-C04 | RuleContext implementação | packages/solver + worker | Spec pronta |
| AMB-C05 | Redis vs job table | infra docker-compose | Designer sugere job table v1 |
| AMB-C06 | requirements.txt | setup Python | G-M04 |

## AUTO-DECIDIDOS (`--auto`)

| ID | Agente | Default aplicado |
|----|--------|------------------|
| AUTO-001 | Paradigm Advisor | Híbrido pragmático (já em paradigm_decision) |
| AUTO-002 | Curator | ⚠️/🔴 → descartar ou MIGRAR com nota |
| AUTO-003 | Strategist | Strangler Fig + Parallel Run |
| AUTO-004 | Designer topology | Modernizar (topology_decision) |
| AUTO-005 | Designer architecture | Primeira proposta aceita |
| AUTO-006 | Screen Translator | Modo modernizado (CLI→SPA) |
| AUTO-007 | Inspector | Critérios paridade sem negociação |

## Histórico

| Data | Agente | Ação |
|------|--------|------|
| 2026-08-10 | curator | 42 regras inventariadas |
| 2026-08-10 | strategist | Estratégia A recomendada e auto-aprovada |
| 2026-08-10 | designer | Fase 2 arquitetura/dados |
| 2026-08-10 | screen_translator | 9 telas MVP |
| 2026-08-10 | inspector | 5 feature files paridade |
| 2026-08-10 | orchestrator | handoff consolidado |
