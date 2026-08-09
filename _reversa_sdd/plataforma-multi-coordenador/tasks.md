# Plataforma Multi-Coordenador — Tarefas

## Fase 1 — Fundação

- [ ] T-01 — Docker Compose (api, postgres, worker)
  - Origem: user-requirements deploy híbrido
  - Confiança: 🟢

- [ ] T-02 — Migrations ERD (coordenador, segmento, grupo, turma, semestre)
  - Origem: erd-complete.md
  - Confiança: 🟡

- [ ] T-03 — Auth JWT + middleware tenant segmento_id
  - Origem: permissions.md
  - Confiança: 🟡

## Fase 2 — Configuração segmento

- [ ] T-04 — CRUD GRUPO com campos customizáveis
  - Origem: user-requirements RBAC
  - Confiança: 🟢

- [ ] T-05 — Associação turma → grupo_id
  - Confiança: 🟢

- [ ] T-06 — Upload entradas → blob + metadados
  - Confiança: 🟡

## Fase 3 — Motor calendário

- [ ] T-07 — Externalizar constantes gerador → BD/GRUPO
  - Confiança: 🟢

- [ ] T-08 — Worker job gerar + RuleContext
  - Origem: geracao-calendario, regras-negocio
  - Confiança: 🟡

- [ ] T-09 — Pipeline verificação pós-job
  - Confiança: 🟡

- [ ] T-10 — Endpoints relatórios
  - Origem: exportacao-relatorios
  - Confiança: 🟡

## Fase 4 — Regras e IA

- [ ] T-11 — API toggles REGRA_CONFIG
  - Origem: ADR-006
  - Confiança: 🟢

- [ ] T-12 — CRUD CUSTOMIZACAO_IA
  - Confiança: 🟢

## Fase 5 — Frontend (ADR-007)

- [ ] T-13 — Scaffold Vite + React + Tailwind + Lucide
  - Confiança: 🟢

- [ ] T-14 — Estado global (Context ou Redux): regras, job solver, segmento
  - Confiança: 🟢

- [ ] T-15 — Telas MVP (login, GRUPOS, upload, toggles, gerar, verificação, download)
  - Confiança: 🟡

- [ ] T-16 — Serviço `frontend` no Docker Compose
  - Confiança: 🟢

## Testes

- [ ] TT-01 — Isolamento tenant A vs B
- [ ] TT-02 — GRUPO conselho refletido no solver
- [ ] TT-03 — E2E upload → gerar → verificar → download
- [ ] TT-04 — Admin Brener lê segmento alheio; coordenador não

## Ordem

T-01 → T-02 → T-03 → T-13 → T-14 → T-04 → T-05 → T-06 → T-07 → T-11 → T-08 → T-09 → T-15 → T-10 → T-16

## Lacunas (🔴)

- PR #14 Must antes deploy? (`questions.md#pergunta-4`)
- Context vs Redux (decisão implementação)
