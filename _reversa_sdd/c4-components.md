# C4 — Componentes (Nível 3)

> Gerado pelo Arquiteto (Reversa) em 2026-08-15

## API Backend (alvo) 🟡

```mermaid
C4Component
    title Componentes — API FastAPI

    Container_Boundary(api, "API Backend") {
        Component(auth, "AuthModule", "JWT/session", "Login 5 coordenadores")
        Component(rules, "RulesCatalogService", "Python", "Catálogo + perfil por rodada")
        Component(ingest, "IngestService", "Python", "Upload grade/modelo/simulados")
        Component(solver, "CalendarSolver", "Python", "Backtracking + Cessoes")
        Component(verify, "CalendarVerifier", "Python", "Checklist 0-11")
        Component(export, "ReportExporter", "Python", "Tabelas, cessões, trocas")
        Component(email, "DonorEmailService", "Python", "Preview + envio manual")
        Component(calendar, "CalendarLifecycle", "Python", "Estados fechado/producao")
        Component(views, "CalendarViewsService", "Python", "Visões e estatísticas")
        Component(docs, "DocumentContextService", "Python", "Contexto uploads + saídas")
        Component(copilot, "ScheduleCopilotService", "Python/API", "Chat copiloto Q&A + propostas")
    }

    Rel(auth, rules, "coordenador_id")
    Rel(ingest, solver, "grade + modelo")
    Rel(ingest, docs, "blobs entrada")
    Rel(rules, solver, "perfil regras ativo")
    Rel(rules, copilot, "RuleSetSnapshot")
    Rel(solver, verify, "alocações")
    Rel(solver, docs, "proposta gerada")
    Rel(verify, calendar, "OK / PROBLEMA")
    Rel(verify, views, "PROBLEMA/AVISO")
    Rel(verify, copilot, "explicações checklist")
    Rel(views, copilot, "estatísticas")
    Rel(docs, copilot, "grounding documentos")
    Rel(copilot, solver, "re-fatoração parcial 🟡")
    Rel(copilot, calendar, "propostas aceitas")
    Rel(calendar, export, "xlsx fechado")
    Rel(export, email, "lista cessões")
    Rel(email, auth, "auditoria enviado_por")
```

## CLI Legado (as-is) 🟢

```mermaid
flowchart TB
    subgraph gerar_calendario.py
        MAIN[main]
        MP[montar_proposta]
        RP[resolver_par]
        R[resolver]
        C[Cessoes]
        ESC[escada]
        W[escrever]
        REL[relatorio]
    end

    subgraph satelite
        VER[verificar_calendario]
        EXP_T[exportar_tabelas_turma]
        EXP_C[exportar_tempos_cedidos]
        EXP_R[exportar_relatorio_trocas]
        EXP_P[exportar_provas_por_professor]
    end

    MAIN --> MP
    MP --> RP --> R
    R --> C
    R --> ESC
    MP --> W --> REL
    W --> VER
    W --> EXP_T & EXP_C & EXP_R & EXP_P
```

### Mapeamento legado → API 🟡

| Componente legado | Componente alvo |
|---|---|
| `montar_proposta` + `resolver*` | `CalendarSolver` |
| `Cessoes` | `CalendarSolver.Cessoes` (módulo) |
| `verificar_calendario.main` | `CalendarVerifier` |
| `exportar_*` | `ReportExporter` |
| Skill Passo 0 + regras | `RulesCatalogService` + UI |
| — | `DonorEmailService` (novo) |
| Skill + chat Cursor/Claude hoje | `ScheduleCopilotService` + `DocumentContextService` (novo 🟡) |
| `commit_github.bat` | `CalendarLifecycle` + Git opcional |

## Frontend (alvo) 🟡 — componentes UI

| Componente UI | Feature Reversa |
|---|---|
| `RulesSelectionWizard` | Seleção regras Tela 1–2 |
| `CalendarEditor` | Refração manual (grid xlsx) |
| `ScheduleCopilotChat` | Chat copiloto pós-geração (Q&A + alterações) 🟡 |
| `ProblemViewsPanel` | Estatísticas / visões alinhadas ao copiloto 🟡 |
| `VerificationPanel` | Checklist PROBLEMA/AVISO |
| `CloseCalendarAction` | Fechar horário |
| `DonorEmailPanel` | Preview + envio e-mail doadores |
