# ADR-008 — Copiloto OpenAI + RAG + ações Python no backend

> Status: **aceito** (requisito usuário 2026-08-15)  
> Confiança: 🟢

## Contexto

O coordenador usa hoje Cursor/Claude com skill e arquivos locais para analisar
e ajustar calendários. A plataforma deve oferecer copiloto embutido pós-geração.

Brener confirmou:

- Provedor LLM: **OpenAI**
- Grounding: **RAG** sobre documentos de base e **xlsx gerado**
- Papel: **copiloto** junto ao coordenador — solução de problemas e
  refração/refatoração conforme solicitações
- Alterações orientadas por **comandos Python** executados no backend

## Decisão

1. **OpenAI API** no backend (`ScheduleCopilotService`); chave nunca no browser.
2. **RAG por rodada** (`RagIndexService`): indexa uploads + Proposta xlsx +
   relatórios + trechos do catálogo de regras; reindex após alterações.
3. **Tool calling** OpenAI mapeado para **`PythonActionBridge`** — whitelist
   de operações (`CalendarSolver`, patch alocação, `CalendarVerifier`).
4. **Sem execução arbitrária** de código Python (`eval`/`exec` proibidos).
5. **Confirmação humana** obrigatória antes de `apply_proposal`.
6. Copiloto pode **mostrar** equivalência legível ao script legado para
   transparência (ex.: "equivalente a re-solver turmas 10C1/10C2 seed 3").

## Consequências

- ✅ Paridade funcional com fluxo Cursor + scripts locais
- ✅ Segurança: superfície de execução controlada
- ✅ Rastreabilidade de tools invocadas por sessão
- ⚠️ Deploy on-prem depende de conectividade OpenAI ou Azure OpenAI
- ⚠️ Dados de professores/turmas trafegam para OpenAI — **mitigado por
  pseudonimização ADR-009**; DPA escola ainda necessário
- ⚠️ Custo tokens + embeddings por rodada

## Alternativas rejeitadas

- **Anthropic / modelo local** — usuário escolheu OpenAI
- **Só leitura estruturada sem RAG** — usuário exige RAG
- **LLM gera Python livre executado no servidor** — risco de segurança

## Evidência

- `.reversa/context/user-requirements.md#Copiloto de IA`
- `_reversa_sdd/addenda/requisito-agente-refraction-api-2026-08-15.md`
