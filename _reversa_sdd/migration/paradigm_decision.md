# Paradigm Decision — calendarioprovas

> Produzido por: Paradigm Advisor | 2026-08-10

## Paradigma legado detectado

| Paradigma | Confiança | Evidência |
|-----------|-----------|-----------|
| **Procedural / script monolítico** | 🟢 | `architecture.md`: CLI batch; `gerar_calendario.py` ~1900 linhas, funções top-level, constantes inline |
| **Constraint satisfaction imperativo** | 🟢 | Backtracking + mutação estado `Cessoes` in-process |

**Híbrido:** N/A — domínio rico na skill, implementação procedural no código.

## Paradigma natural da stack alvo

| Camada | Paradigma natural | Confiança |
|--------|-------------------|-----------|
| API FastAPI | OO leve + DI (routers, services, repos) | 🟢 |
| Frontend React | Component-driven + hooks; estado global Context/Redux | 🟢 |
| Solver worker | **Procedural preservado** — wrap do legado, não reescrever algoritmo | 🟢 |

## Gap de paradigma

| Gap | Severidade | Tratamento decidido |
|-----|------------|---------------------|
| Script monolítico → serviços + BD | Alta | **Strangler:** extrair `solver/` como lib; worker chama funções existentes |
| Constantes → config persistida | Média | GRUPO + semestre no PostgreSQL |
| CLI stdout → API JSON + jobs | Média | Job queue + status polling |

## Decisão do usuário

**Paradigma alvo:** **Híbrido pragmático**

- Domínio/API: camadas (router → service → repository) com DI FastAPI
- Solver: **preservar procedural** do legado em módulo isolado `packages/solver/`
- Frontend: componentes React funcionais

Brener confirmou reutilizar Python existente (`user-requirements.md`).

## Sinais para agentes posteriores

- Não reescrever backtracking em estilo funcional puro
- Externalizar config antes de multi-tenant completo
- Testes de paridade comparam xlsx gerado plataforma vs CLI
