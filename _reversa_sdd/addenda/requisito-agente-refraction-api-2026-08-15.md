# Addendum — Agente de refração via API

> 2026-08-15 | Origem: `.reversa/context/user-requirements.md#Agente de refração conectado via API`  
> Confiança: 🟢 requisito usuário | 🟡 detalhes de implementação

## Resumo

A plataforma deve permitir conectar um **agente de IA via API** para apoiar
a **refração** do calendário: diagnosticar problemas de tempo/cessão/regras
usando **visões analíticas** e devolver **propostas estruturadas** que o
coordenador confirma antes de persistir.

## Componentes alvo

| Componente | Responsabilidade |
|---|---|
| `RefractionAgentGateway` | Orquestra sessão, contexto, LLM, apply |
| `CalendarViewsService` | Visões JSON (turma, semana, cessão, regra, slots) |
| `CalendarVerifier` | Fonte de PROBLEMA/AVISO para o agente |
| `CalendarSolver` | Re-fatoração parcial sob demanda do agente |
| `RulesCatalogService` | RuleSetSnapshot compartilhado |

## Endpoints provisórios (🟡)

| Método | Caminho | Propósito |
|--------|---------|-----------|
| GET | `/api/v1/calendars/{id}/views/{viewType}` | Visão analítica |
| GET | `/api/v1/calendars/{id}/verification` | Checklist atual |
| POST | `/api/v1/calendars/{id}/agent/sessions` | Inicia sessão |
| POST | `/api/v1/calendars/{id}/agent/sessions/{sid}/messages` | Turno chat / instrução |
| GET | `/api/v1/calendars/{id}/agent/sessions/{sid}/proposals` | Propostas pendentes |
| POST | `/api/v1/calendars/{id}/agent/proposals/{pid}/apply` | Aplica proposta aceita |
| POST | `/api/v1/calendars/{id}/agent/proposals/{pid}/reject` | Rejeita proposta |

## Tipos de visão sugeridos (v1 🟡)

- `conflicts-by-class` — provas/regras violadas por turma
- `conflicts-by-week` — carga semanal > limite
- `donations-by-teacher` — cessões agrupadas por doador
- `sibling-pairs` — coordenação 10C1/10C2 etc.
- `rule-violations` — agrupado por id de regra (R-P1, C4…)
- `candidate-slots` — slots livres para mover prova `{turma, disc}`

## Features Reversa impactadas

- `plataforma-multi-coordenador` — **H**
- `verificacao-calendario` — **M** (feed de problemas)
- `geracao-calendario` — **M** (re-fatoração parcial)
- `regras-negocio` — **M** (RuleSetSnapshot)

## Lacunas 🔴

- Provedor LLM e deploy on-prem sem internet
- Chat UI vs API-only
- Autonomia do agente
