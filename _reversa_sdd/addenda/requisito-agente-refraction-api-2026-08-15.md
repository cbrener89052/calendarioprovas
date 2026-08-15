# Addendum — Copiloto OpenAI + RAG + ações Python

> 2026-08-15 | Origem: `.reversa/context/user-requirements.md#Copiloto de IA`  
> **Atualizado 2026-08-15:** OpenAI, RAG, refração colaborativa — ADR-008  
> Confiança: 🟢 requisito usuário | 🟡 detalhes de implementação

## Resumo

Copiloto **OpenAI** embutido na plataforma, com **RAG** sobre documentos de
base e **xlsx gerado**, trabalhando **junto** do coordenador para analisar,
responder perguntas e **refatorar horários** via **ações Python** controladas
no backend (tool calling), com confirmação humana.

## Decisões 🟢

| Item | Valor |
|------|-------|
| LLM | **OpenAI API** |
| Grounding | **RAG** (uploads + Proposta xlsx + derivados + regras) |
| Modo | Copiloto colaborativo — problemas + refração/refatoração |
| Execução | `PythonActionBridge` → solver / patch / verificador |
| Segurança | Whitelist tools; sem `eval`/`exec` |

## Papéis do copiloto

| Modo | Gatilho | Saída |
|------|---------|-------|
| **Analista (Q&A)** | Pergunta | Resposta + citações RAG 🟢/🟡 |
| **Diagnóstico** | PROBLEMA verificador | Plano de correção |
| **Refração/refatoração** | Solicitação do coordenador | Tools Python + preview + confirmação |

## Componentes alvo

| Componente | Responsabilidade |
|---|---|
| `ScheduleCopilotService` | OpenAI chat + tool loop |
| `RagIndexService` | Chunk, embed, search (OpenAI embeddings 🟡) |
| `DocumentContextService` | Ingest blobs → corpus RAG |
| `PythonActionBridge` | Tool calls → Python backend |
| `CalendarViewsService` | Estatísticas JSON |
| `CalendarSolver` / `CalendarVerifier` | Execução real |

## OpenAI tools (v1 provisória 🟡)

| Tool | Backend Python |
|------|----------------|
| `rag_search` | `RagIndexService.search` |
| `get_calendar_view` | `CalendarViewsService` |
| `get_verification_report` | `CalendarVerifier` |
| `propose_allocation_patch` | patch preview (openpyxl layer) |
| `run_partial_solver` | `CalendarSolver.montar_proposta` subset |
| `apply_proposal` | persist + reindex RAG + verify |

## Corpus RAG (Must)

- Grade, modelo, simulados, siglas, referências (uploads)
- **Proposta_3.xlsx** e exports após cada alteração aceita
- Relatório trocas, checklist verificador
- Trechos catálogo regras (skill espelhada)

## Endpoints provisórios (🟡)

| Método | Caminho | Propósito |
|--------|---------|-----------|
| POST | `/api/v1/calendars/{id}/copilot/sessions` | Nova sessão |
| POST | `/api/v1/calendars/{id}/copilot/sessions/{sid}/messages` | Mensagem |
| POST | `/api/v1/calendars/{id}/copilot/rag/reindex` | Reindex pós-alteração |
| POST | `/api/v1/calendars/{id}/copilot/proposals/{pid}/apply` | Confirma + executa Python |

## Lacunas 🔴

- Modelo OpenAI específico
- Azure OpenAI para on-prem
- Política PII / DPA escola
- Copiloto read-only pós-fechar
