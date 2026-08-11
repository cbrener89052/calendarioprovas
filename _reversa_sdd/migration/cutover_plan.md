---
schemaVersion: 1
generatedAt: 2026-08-10T02:05:00Z
reversa:
  version: "1.2.58"
kind: cutover_plan
producedBy: strategist
---

# Cutover Plan

> Estratégia: **Strangler Fig + Parallel Run (solver)**  
> Janela alvo: **início de semestre** (fora do período de provas em curso)

## Pré-requisitos

- [ ] Parallel Run: ≥1 semestre piloto com diff xlsx CLI vs plataforma = 0 divergências críticas
- [ ] Verificador plataforma OK em 100% dos jobs piloto
- [ ] 5 contas coordenador + Brener admin configuradas
- [ ] Docker Compose on-prem testado (`docker compose up`)
- [ ] Backup PostgreSQL + blobs configurado
- [ ] Rollback documentado (reativar CLI local)

## Fases

### Fase 0 — Preparação (Strangler)
| Passo | Owner | Duração est. |
|-------|-------|--------------|
| Extrair `packages/solver/` do legado | dev | — |
| API + worker MVP | dev | — |
| Import entradas semestre atual para blob | dev | 2h |

### Fase 1 — Parallel Run
| Passo | Owner | Duração est. |
|-------|-------|--------------|
| Gerar calendário CLI (referência) | Brener | 1h |
| Gerar calendário plataforma (mesmas entradas) | Brener | 1h |
| Diff xlsx + relatórios | dev/automação | 2h |
| Verificador ambos OK | auto | — |
| Repetir para 2º segmento piloto | coord | 2h |

### Fase 2 — Cutover
| Passo | Owner | Duração est. |
|-------|-------|--------------|
| Comunicar coords: plataforma é canal oficial | Brener | — |
| Desabilitar instruções CLI no README operacional | dev | 30min |
| Monitorar jobs 1ª semana | dev/ops | contínuo |

## Critérios go/no-go

| Critério | Go | No-go |
|----------|-----|-------|
| Paridade xlsx | 0 diffs críticos em piloto | Qualquer violação cessão/LP-LIT-RED |
| Verificador | 100% OK piloto | Erro crítico não explicado |
| Isolamento tenant | Teste A≠B passa | Vazamento segmento |
| Performance | Job ≤ 2× CLI (brief) | Timeout sistemático |

## Rollback

1. Reativar fluxo CLI documentado em `legacy/`
2. Coordenadores continuam com xlsx local
3. Dados plataforma preservados para retry
4. Post-mortem em 48h

## Pós-cutover

- Manter `legacy/` por 1 semestre como referência
- Sync skill → catálogo BD após cada PR relevante
- Avaliar descomissionar CLI após 2º semestre estável
