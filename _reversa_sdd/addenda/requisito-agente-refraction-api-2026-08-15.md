# Addendum — Copiloto de IA (agente analista do horário)

> 2026-08-15 | Origem: `.reversa/context/user-requirements.md#Copiloto de IA`  
> Confiança: 🟢 requisito usuário | 🟡 detalhes de implementação

## Resumo

Após **análise das entradas** e **geração do horário**, a plataforma oferece
um **chat copiloto** (via API) equivalente ao fluxo atual no **Cursor /
Claude Code**: o agente **responde perguntas**, **analisa estatísticas** do
calendário gerado e dos **documentos de base** enviados, e **sugere
alterações** na refração — sempre com confirmação humana.

## Papéis do copiloto

| Modo | Gatilho | Saída |
|------|---------|-------|
| **Analista (Q&A)** | Pergunta em linguagem natural | Resposta citando dados + confiança 🟢/🟡 |
| **Estatístico** | Pergunta ou painel de visões | Agregações (cessões, semanas, professores) |
| **Copiloto de alteração** | Pedido de mudança | Proposta estruturada + diff preview |

## Componentes alvo

| Componente | Responsabilidade |
|---|---|
| `ScheduleCopilotService` | Chat, contexto, LLM, propostas |
| `DocumentContextService` | Grounding: blobs entrada + saída gerada |
| `CalendarViewsService` | Visões/estatísticas JSON |
| `CalendarVerifier` | PROBLEMA/AVISO para explicações |
| `CalendarSolver` | Re-fatoração parcial sob demanda |
| `RulesCatalogService` | RuleSetSnapshot + catálogo skill |

## Contexto da sessão (Must)

- Grade, modelo, simulados, siglas, referências do semestre (uploads)
- Proposta gerada, relatório trocas, exports
- Resultado verificador + visões estatísticas
- RuleSetSnapshot da rodada

## Endpoints provisórios (🟡)

| Método | Caminho | Propósito |
|--------|---------|-----------|
| GET | `/api/v1/calendars/{id}/views/{viewType}` | Estatística / visão |
| GET | `/api/v1/calendars/{id}/verification` | Checklist |
| GET | `/api/v1/calendars/{id}/context/summary` | Resumo documentos base + gerados |
| POST | `/api/v1/calendars/{id}/copilot/sessions` | Nova sessão chat |
| POST | `/api/v1/calendars/{id}/copilot/sessions/{sid}/messages` | Pergunta ou instrução |
| GET | `/api/v1/calendars/{id}/copilot/sessions/{sid}/proposals` | Propostas pendentes |
| POST | `/api/v1/calendars/{id}/copilot/proposals/{pid}/apply` | Aplica proposta |
| POST | `/api/v1/calendars/{id}/copilot/proposals/{pid}/reject` | Rejeita proposta |

## UI alvo

- `ScheduleCopilotChat` — chat embutido pós-geração
- `ProblemViewsPanel` — visões alinhadas às respostas do agente

## Equivalência legado

| Hoje (Cursor/Claude) | Plataforma |
|---|---|
| Skill `calendario-provas` | Catálogo regras + system prompt |
| Arquivos do repo / uploads | Blob + `DocumentContextService` |
| Perguntas no chat | `ScheduleCopilotChat` |
| Edição manual xlsx | Grid + propostas aceitas do copiloto |

## Features Reversa impactadas

- `plataforma-multi-coordenador` — **H**
- `verificacao-calendario` — **M**
- `geracao-calendario` — **M**
- `regras-negocio` — **M**
- `exportacao-relatorios` — **L** (contexto derivados)

## Lacunas 🔴

- Provedor LLM (Anthropic/OpenAI) e on-prem
- RAG vs parse estruturado de xlsx/pdf
- Copiloto read-only após fechar horário
