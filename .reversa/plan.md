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

**Histórico de calendários (2026-08-11):** cada geração persiste automaticamente;
tela única **Calendários** (`/calendarios`) consulta períodos anteriores e acessa versões geradas (ADR-009, RF-19).

**Verificação (2026-08-11):** `verificar_calendario.py` audita xlsx gravado (PROBLEMA vs AVISO); worker plataforma deve replicar (ADR-010).

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

## Fase 6: Migração 🚀

- [x] **Paradigm Advisor** — `paradigm_decision.md` (híbrido pragmático)
- [x] **Curator** — `target_business_rules.md`, `discard_log.md`
- [x] **Strategist** — Strangler Fig + Parallel Run; riscos e cutover
- [x] **Designer** — topologia moderna + arquitetura/dados alvo
- [x] **Screen Translator** — 9 telas MVP (modo modernizado)
- [x] **Inspector** — `parity_specs.md` + 5 cenários Gherkin
- [x] **Handoff** — `_reversa_sdd/migration/handoff.md`

## Próximo passo

**Time de Migração concluído** (2026-08-10, modo `--auto`).

Fluxos disponíveis:

- `/reversa-reconstructor`: implementar sistema novo — fonte **migração** (`_reversa_sdd/reconstruction-plan.md`, 14 tarefas).
- Revisar itens auto-decididos em `_reversa_sdd/migration/ambiguity_log.md` antes do cutover.
