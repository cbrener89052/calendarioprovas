# Migration Brief — calendarioprovas

> Gerado pelo orquestrador `/reversa-migrate` em 2026-08-10  
> Brief pré-preenchido a partir de `.reversa/context/user-requirements.md` e respostas Brener (Fase 5)

## Objetivo da migração

Evoluir o sistema **CLI + arquivos locais** para uma **plataforma web multi-coordenador** que preserve a lógica de geração/verificação de calendários de provas (Proposta 3), permitindo que 5 coordenadores operem segmentos isolados com regras configuráveis e customizações IA.

## Métricas de sucesso

- Calendário Proposta 3 gerado na plataforma **equivalente** ao CLI para o mesmo semestre (paridade xlsx + verificador OK)
- Isolamento tenant: coordenador A não acessa dados de B
- Tempo de job de geração ≤ 2× CLI atual para 8 turmas C
- Brener (admin) gerencia catálogo de regras; coords configuram toggles e GRUPOS

## Restrições

- **Técnicas:** Manter solver Python (`gerar_calendario.py` core); FastAPI + PostgreSQL; frontend React Vite (ADR-007)
- **Operacionais:** Deploy híbrido — nuvem + Docker Compose on-prem
- **Regulatórias:** Regras institucionais da skill `calendario-provas` são fonte viva

## Fatores de risco conhecidos

- Constantes hardcoded no gerador — externalização para BD/GRUPO
- Acoplamento verificador ↔ gerador
- Camada IA (custo/latência) no verificador + relatório
- Context vs Redux — decisão pendente na implementação

## Stakeholders

| Nome / papel | Responsabilidade |
|---|---|
| Brener | Admin institucional, mantenedor skill, primeiro usuário |
| 5 coordenadores | Operadores de segmento |
| Equipe docente | Consumidores de relatórios exportados |

## Stack alvo

- **Backend:** Python 3.11+, FastAPI, worker assíncrono (solver)
- **Banco:** PostgreSQL 16
- **Frontend:** React 18 + Vite + Tailwind CSS + Lucide React
- **Estado UI:** React Context ou Redux
- **Storage:** S3 (nuvem) / volume local (Docker)
- **Infra:** Docker Compose; auth JWT
- **IA:** API externa (OpenAI/Anthropic) para customizações — configurável

## Escopo declarado

- **Incluído:** geracao, verificacao, exportacao, extracao-grade (upload), regras-negocio, plataforma-multi-coordenador
- **Excluído (v1):** analise-historica (v2), scripts `.bat` git sync (substituídos por CI)

## Notas livres

- PR #18 implementado: LP/LIT/RED ≥10 dias, SEED=3, folga_extra por turma
- Customização IA: verificador + relatório auxiliar (Brener 2026-08-09)
