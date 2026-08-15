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

**Atualização 2026-08-15:** fluxo de **seleção de regras** antes da
fatoração/refração do horário e revisão antes de fechar — ver mesma seção
em `user-requirements.md`.

**Atualização 2026-08-15 (2):** **envio de e-mail** aos professores que
cedem tempo — ação manual do coordenador após calendário estável, não a
cada refração — ver `user-requirements.md`.

**Stack acordada (preliminar):** Python (FastAPI) + PostgreSQL + login
individual (5 coord.) + deploy nuvem com opção Docker/on-prem local.

---

## Fase 1: Reconhecimento 🔍

- [x] **Scout** — Mapeamento de estrutura de pastas e tecnologias
- [x] **Scout** — Análise de dependências e gerenciadores de pacotes
- [x] **Scout** — Identificação de entry points, CI/CD e configurações

## Decisão de organização das specs 🗂️

> **Decidido em 2026-08-15:** organização **por features** (`granularity = feature`), persistido em `.reversa/config.toml`.

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

- [ ] **Redator** — Specs SDD por componente
- [ ] **Redator** — OpenAPI (se aplicável)
- [ ] **Redator** — User Stories (se aplicável)
- [ ] **Redator** — Code/Spec Matrix

## Fase 5: Revisão ✅

- [ ] **Revisor** — Revisão cruzada de specs
- [ ] **Revisor** — Resolução de lacunas com o usuário
- [ ] **Revisor** — Relatório de confiança final

---

## Agentes Independentes

> Execute estes agentes quando os recursos estiverem disponíveis — podem rodar em qualquer fase.

- [ ] **Visor** — Análise de interface via screenshots
- [ ] **Data Master** — Análise completa do banco de dados
- [ ] **Design System** — Extração de tokens de design
- [ ] **Tracer** — Análise dinâmica (requer sistema acessível)

---

## Próximo passo

**Em andamento (2026-08-15):** Redator — specs SDD por feature. Unit `geracao-calendario` concluída; pendentes: `verificacao-calendario`, `exportacao-relatorios`, `extracao-grade`, `analise-historica`, `regras-negocio`, `plataforma-multi-coordenador` + globais (OpenAPI, user-stories, code-spec-matrix).

Após o Time de Descoberta concluir e o `_reversa_sdd/` estar populado, você pode disparar um dos fluxos seguintes:

- `/reversa-migrate`: orquestrador do **Time de Migração** (Paradigm Advisor → Curator → Strategist → Designer → Screen Translator → Inspector). Gera as specs do sistema novo. Saída em `_reversa_sdd/migration/` e `_reversa_sdd/screens/`.
- `/reversa-reconstructor`: gera plano bottom-up para reimplementar o software a partir das specs do legado (uma tarefa por sessão).
