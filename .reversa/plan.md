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

**Stack acordada (preliminar):** Python (FastAPI) + PostgreSQL + login
individual (5 coord.) + deploy nuvem com opção Docker/on-prem local.

---

## Fase 1: Reconhecimento 🔍

- [x] **Scout** — Mapeamento de estrutura de pastas e tecnologias
- [x] **Scout** — Análise de dependências e gerenciadores de pacotes
- [x] **Scout** — Identificação de entry points, CI/CD e configurações

## Decisão de organização das specs 🗂️

> Entre o Scout e o Arqueólogo, o Reversa pergunta como você quer organizar as specs (por módulo, caso de uso, endpoint, híbrida, por features ou customizada). A escolha fica persistida em `.reversa/config.toml` na seção `[specs]` e não será reperguntada em execuções futuras. Para reapresentar o menu, remova manualmente a seção.

## Fase 2: Escavação 🏗️

> O Reversa preenche esta seção com os módulos reais após o Scout concluir o reconhecimento.

- [ ] **Arqueólogo** — Análise do módulo `geracao-calendario`
- [ ] **Arqueólogo** — Análise do módulo `verificacao-calendario`
- [ ] **Arqueólogo** — Análise do módulo `exportacao-relatorios`
- [ ] **Arqueólogo** — Análise do módulo `extracao-grade`
- [ ] **Arqueólogo** — Análise do módulo `analise-historica`
- [ ] **Arqueólogo** — Análise do módulo `regras-negocio`
- [ ] **Arqueólogo** — Análise do módulo `plataforma-multi-coordenador` (evolução futura)

## Fase 3: Interpretação 🧠

- [ ] **Detetive** — Arqueologia Git e ADRs retroativos
- [ ] **Detetive** — Regras de negócio implícitas e máquinas de estado
- [ ] **Detetive** — Matriz de permissões (RBAC/ACL) — **prioridade: multi-coordenador**
- [ ] **Arquiteto** — Diagramas C4 (Contexto, Containers, Componentes)
- [ ] **Arquiteto** — ERD completo (**incluir modelo de dados multi-coordenador**)
- [ ] **Arquiteto** — Spec Impact Matrix — **legado arquivo-local → plataforma com BD**

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

Após o Time de Descoberta concluir e o `_reversa_sdd/` estar populado, você pode disparar um dos fluxos seguintes:

- `/reversa-migrate`: orquestrador do **Time de Migração** (Paradigm Advisor → Curator → Strategist → Designer → Screen Translator → Inspector). Gera as specs do sistema novo. Saída em `_reversa_sdd/migration/` e `_reversa_sdd/screens/`.
- `/reversa-reconstructor`: gera plano bottom-up para reimplementar o software a partir das specs do legado (uma tarefa por sessão).
