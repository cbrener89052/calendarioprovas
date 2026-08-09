# ADR-006 — Segmento por coordenador e regras configuráveis

**Status:** Aceito  
**Data:** 2026-08-09  
**Confiança:** 🟢 (declarado por Brener)

## Contexto

Plataforma multi-coordenador (5 usuários). Cada escola/segmento tem características diferentes. Regras hoje hardcoded; futuro menu deve permitir flexibilidade sem fork de código para cada coordenador.

## Decisão

1. **Segmento de atuação** — cada coordenador configura turmas, períodos e parâmetros do seu contexto escolar.
2. **Regras codificadas** — catálogo derivado da skill; **ativar/desativar** por coordenador/semestre via UI.
3. **Customizações IA** — adaptações que não entram no solver; IA interpreta configs do coordenador (texto + contexto do segmento).

## Alternativas consideradas

| Opção | Rejeitada porque |
|---|---|
| Fork de código por coordenador | Insustentável com 5+ usuários |
| Só IA, sem toggles | Regras críticas (cessão) precisam ser determinísticas |
| Só hardcode | Não escala multi-segmento |

## Consequências

- ERD: `segmento`, `regra_catalogo`, `regra_config`, `customizacao_ia`
- Solver recebe `RuleContext` filtrado pelos toggles ativos
- Fase Redator: feature `plataforma-multi-coordenador` + `regras-configuraveis`
- PR #14 permanece lacuna de código até implementação explícita
