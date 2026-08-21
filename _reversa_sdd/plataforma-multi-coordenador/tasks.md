# Plataforma Multi-Coordenador — Tarefas

## Fase 1 — Fundação

- [ ] T-01, Scaffold FastAPI + PostgreSQL + Docker Compose
- [ ] T-02, Auth conta compartilhada + PIN por coordenador (5 PINs, auditoria por PIN — ADR-015)
- [ ] T-02b, `EnemWeekConfigPanel` + API persistência (ADR-015)
- [ ] T-03, ERD migrações (usuário, calendário, blob)
- [ ] T-04, CRUD calendário + estados

## Fase 2 — Ingestão

- [ ] T-05, GradeParserService (ver extracao-grade)
- [ ] T-06, CalendarBlockPicker + constraints API
- [ ] T-07, ExamCatalogEditor + intake opcional

## Fase 3 — Core

- [ ] T-08, RulesSelectionWizard + snapshot
- [ ] T-09, CalendarSolver job + escrever blob
- [ ] T-10, CalendarVerifier integrado
- [ ] T-11, CalendarPreviewView + download Excel

## Fase 4 — Pós-geração

- [ ] T-12, ReportExporter
- [ ] T-13, ScheduleCopilotService + RAG
- [ ] T-14, DonorEmailPanel
- [ ] T-15, CloseCalendarAction + branch producao 🟡

Ordem: Fase 1 → 2 → 3 → 4 (paralelizar T-05..T-07 após T-04)
