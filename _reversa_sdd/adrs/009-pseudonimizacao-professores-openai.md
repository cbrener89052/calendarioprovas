# ADR-009 — Pseudonimização de professores para OpenAI

> Status: **aceito** (requisito usuário 2026-08-15)  
> Confiança: 🟢 intenção | 🟡 detalhes criptográficos

## Contexto

O copiloto OpenAI precisa analisar horários que contêm **siglas de
professores** e relações doador/solicitante de cessões. Enviar siglas e
nomes reais à API OpenAI aumenta exposição de PII.

Brener perguntou se o backend Python pode **anonimizar** antes do envio
(atribuir código por professor) e **reverter** ao receber — mantendo o
solver e o coordenador trabalhando com dados reais localmente.

## Decisão

Implementar camada **`ProfessorPseudonymService`** no backend FastAPI:

1. **Mapeamento por rodada** (`calendario_id` + versão):
   - sigla real (ex.: `MFo`) → token opaco (ex.: `PROF_7K2M`)
   - tabela em PostgreSQL; **não** enviada à OpenAI
2. **Antes de OpenAI** (prompt, RAG chunks, tool outputs destinados ao LLM):
   - substituir siglas/nomes de professor por tokens
   - horários (tempos 1–11, semanas, turmas) permanecem 🟢 — não são PII
3. **Respostas OpenAI → coordenador**:
   - **de-tokenização** (lookup inverso) antes de exibir no chat UI
4. **Execução Python** (`CalendarSolver`, patch, verificador):
   - sempre com **siglas reais** — tokens só na fronteira OpenAI
5. **Mensagens do coordenador** que citam siglas reais:
   - tokenizadas no backend antes de enviar ao modelo
6. **Índice RAG**:
   - armazenar versão **tokenizada** para retrieval enviado ao embedding/chat
   - opcional: manter corpus real criptografado at-rest para reindex local 🟡

### Terminologia (precisão)

| Termo coloquial | Implementação |
|---|---|
| "Anonimizar" | **Pseudonimizar** — substituir por token reversível |
| "Descriptografar" | **De-tokenizar** — lookup `PROF_*` → sigla real |
| Criptografia (opcional) | AES para coluna `sigla_real` at-rest ou blob de mapping 🟡 |

Pseudonimização **não** é anonimização irreversível; reduz PII direta na OpenAI.

## Fluxo

```
Coordenador: "quantas cessões MFo?"
  → Backend tokeniza: "quantas cessões PROF_7K2M?"
  → OpenAI responde com PROF_7K2M
  → Backend de-tokeniza UI: "MFo — 4 cessões..."
  → Tools Python usam sigla real MFo internamente
```

## Consequências

- ✅ Siglas/nomes não aparecem em texto enviado à OpenAI (apenas tokens)
- ✅ Solver/verificador inalterados — dados reais no processo Python
- ✅ Coordenador vê siglas reais na interface
- ⚠️ Re-identificação ainda possível por padrão do horário (turma + tempo)
- ⚠️ OpenAI API retention / DPA escola ainda necessários
- ⚠️ Mapping leak = exposição — proteger tabela + logs (nunca logar prompt real)

## Alternativas rejeitadas

- **Enviar siglas reais** — maior exposição PII
- **Anonimização irreversível** — impede UI e tools Python legíveis
- **Tokenização só no frontend** — chave/mapping no browser seria inseguro

## Evidência

- `.reversa/context/user-requirements.md#Privacidade — pseudonimização`
