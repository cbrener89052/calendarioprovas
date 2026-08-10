---
schemaVersion: 1
generatedAt: 2026-08-10T02:05:00Z
reversa:
  version: "1.2.58"
kind: risk_register
producedBy: strategist
---

# Risk Register

## Riscos críticos

| ID | Risco | Prob. | Impacto | Mitigação | Contingência | Owner |
|----|-------|-------|---------|-----------|--------------|-------|
| R-01 | Divergência xlsx plataforma vs CLI | média | crítico | Parallel Run semestre piloto; diff automatizado | Manter CLI como fallback | a definir (dev) |
| R-02 | Constantes hardcoded impedem multi-segmento | alta | alto | Externalizar para GRUPO/RuleContext antes prod | Bloquear 2º coordenador até refactor | a definir |
| R-03 | Worker timeout em backtracking pesado | média | alto | Limites MAX_NOS; fila com timeout configurável | Retry + alerta coordenador | a definir (ops) |

## Riscos de paradigma

| ID | Risco | Prob. | Impacto | Mitigação | Owner |
|----|-------|-------|---------|-----------|-------|
| R-04 | Reescrita acidental do solver | baixa | crítico | `packages/solver/` read-only wrap; code review | a definir |
| R-05 | RuleContext incompleto vs toggles BD | média | alto | Testes paridade por toggle on/off | a definir |

## Riscos de dados

| ID | Risco | Prob. | Impacto | Mitigação | Owner |
|----|-------|-------|---------|-----------|-------|
| R-06 | Migração entradas legado → blob | baixa | médio | Script one-shot + checksum | a definir |
| R-07 | Perda blobs on-prem sem backup | baixa | alto | Volume persistente + backup diário | a definir (ops) |

## Riscos operacionais

| ID | Risco | Prob. | Impacto | Mitigação | Owner |
|----|-------|-------|---------|-----------|-------|
| R-08 | Cutover no meio do semestre escolar | média | alto | Janela entre semestres; go/no-go formal | Brener |
| R-09 | Custo/latência IA customizações | média | médio | IA opcional; cache relatório | a definir |
| R-10 | On-prem sem internet (IA) | alta | baixo | Verificador determinístico funciona offline | Brener |

## Riscos organizacionais

| ID | Risco | Prob. | Impacto | Mitigação | Owner |
|----|-------|-------|---------|-----------|-------|
| R-11 | 5 coords treinamento UI nova | média | médio | MVP simples; docs fluxo semestre | Brener |
| R-12 | Context vs Redux indecisão atrasa frontend | baixa | baixo | Decidir na T-13 implementação | a definir |

## Histórico

| Data | Alteração |
|------|-----------|
| 2026-08-10 | Versão inicial pós-Strategist |
