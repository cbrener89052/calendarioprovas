# Plano de Exploração — calendarioprovas

> Criado pelo Reversa em 2026-08-08
> Marque cada tarefa com ✅ quando concluída.
> Você pode editar este plano antes de iniciar: adicione, remova ou reordene tarefas conforme necessário.

---

## Visão futura declarada pelo usuário (2026-08-09)

O sistema será usado por **vários coordenadores** da instituição. A evolução
prevista inclui **banco de dados** para persistir entradas (horários, modelos,
simulados, siglas) e saídas (calendários, relatórios) **por coordenador**.

Detalhes em `.reversa/context/user-requirements.md`.

**Sincronização de regras (skill ↔ Reversa):** enquanto Brener atualiza a skill no Claude Code, seguir `.reversa/context/sync-regras.md`. Fontes vivas listadas em `.reversa/context/sources.json`.

**Stack acordada (preliminar):** Python (FastAPI) + PostgreSQL + login
individual (5 coord.) + deploy nuvem com opção Docker/on-prem local.

---

## Fase 1: Reconhecimento 🔍

- [x] **Scout** — Mapeamento de estrutura de pastas e tecnologias
- [x] **Scout** — Análise de dependências e gerenciadores de pacotes
- [x] **Scout** — Identificação de entry points, CI/CD e configurações

## Decisão de organização das specs 🗂️

- [x] **Organização por features** — escolha 5, persistida em `.reversa/config.toml` (`layout = "feature-folder"`)

## Fase 2: Escavação 🏗️

> O Reversa preenche esta seção com os módulos reais após o Scout concluir o reconhecimento.

- [x] **Arqueólogo** — Análise do módulo `geracao-calendario`
- [x] **Arqueólogo** — Análise do módulo `verificacao-calendario`
- [x] **Arqueólogo** — Análise do módulo `exportacao-relatorios`
- [x] **Arqueólogo** — Análise do módulo `extracao-grade`
- [x] **Arqueólogo** — Análise do módulo `analise-historica`
- [x] **Arqueólogo** — Análise do módulo `regras-negocio`
- [x] **Arqueólogo** — Análise do módulo `plataforma-multi-coordenador` (evolução futura)

## Fase 3: Interpretação 🧠

- [x] **Detetive** — Arqueologia Git e ADRs retroativos
- [x] **Detetive** — Regras de negócio implícitas e máquinas de estado
- [x] **Detetive** — Matriz de permissões (RBAC/ACL) — **prioridade: multi-coordenador**
- [x] **Arquiteto** — Diagramas C4 (Contexto, Containers, Componentes)
- [x] **Arquiteto** — ERD completo (**incluir modelo de dados multi-coordenador**)
- [x] **Arquiteto** — Spec Impact Matrix — **legado arquivo-local → plataforma com BD**

## Fase 4: Geração 📝

- [x] **Redator** — Specs SDD por componente (7 features × requirements/design/tasks)
- [x] **Redator** — OpenAPI (`_reversa_sdd/openapi/calendarioprovas.yaml`)
- [x] **Redator** — User Stories (`_reversa_sdd/user-stories/fluxo-calendario-semestre.md`)
- [x] **Redator** — Code/Spec Matrix (`_reversa_sdd/traceability/code-spec-matrix.md`)

## Fase 5: Revisão ✅

- [x] **Revisor** — Revisão cruzada de specs (7 features, 0 contradições críticas)
- [x] **Revisor** — Lacunas documentadas (`questions.md` — 4 perguntas para Brener)
- [x] **Revisor** — Relatório de confiança final (`confidence-report.md` — 77,5%)

---

## Agentes Independentes

> Execute estes agentes quando os recursos estiverem disponíveis — podem rodar em qualquer fase.

- [ ] **Visor** — Análise de interface via screenshots
- [ ] **Data Master** — Análise completa do banco de dados
- [ ] **Design System** — Extração de tokens de design
- [ ] **Tracer** — Análise dinâmica (requer sistema acessível)

---

## Próximo passo

**Time de Descoberta concluído** — 4/4 perguntas respondidas. PR #14 Must deploy; Claude agendado.

Fluxos disponíveis:

- `/reversa-migrate`: orquestrador do **Time de Migração** (Paradigm Advisor → Curator → Strategist → Designer → Screen Translator → Inspector). Gera as specs do sistema novo. Saída em `_reversa_sdd/migration/` e `_reversa_sdd/screens/`.
- `/reversa-reconstructor`: gera plano bottom-up para reimplementar o software a partir das specs do legado (uma tarefa por sessão).
