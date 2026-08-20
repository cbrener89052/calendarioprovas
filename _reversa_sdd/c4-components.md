# C4 — Componentes (Nível 3)

> Gerado pelo Arquiteto (Reversa) em 2026-08-15

## API Backend (alvo) 🟡

```mermaid
C4Component
    title Componentes — API FastAPI

    Container_Boundary(api, "API Backend") {
        Component(auth, "AuthModule", "JWT/session", "Login 5 coordenadores")
        Component(rules, "RulesCatalogService", "Python", "Catálogo + perfil por rodada")
        Component(ingest, "IngestService", "Python", "Upload grade, catálogo, simulados")
        Component(intake, "IntakeTemplateService", "Python", "Máscaras provas + bloqueios")
        Component(constraints, "CalendarConstraintsService", "Python", "Bloqueios persistidos")
        Component(catalog, "ExamCatalogService", "Python", "ExamCatalog normalizado")
        Component(layout, "CalendarLayoutTemplate", "blob", "Klausurplan institucional")
        Component(solver, "CalendarSolver", "Python", "Backtracking + Cessoes")
        Component(verify, "CalendarVerifier", "Python", "Checklist 0-11")
        Component(export, "ReportExporter", "Python", "Tabelas, cessões, trocas")
        Component(email, "DonorEmailService", "Python", "Preview + envio manual")
        Component(calendar, "CalendarLifecycle", "Python", "Estados fechado/producao")
        Component(views, "CalendarViewsService", "Python", "Visões e estatísticas")
        Component(rag, "RagIndexService", "Python + OpenAI", "RAG documentos + xlsx")
        Component(docs, "DocumentContextService", "Python", "Ingest blobs → corpus")
        Component(bridge, "PythonActionBridge", "Python", "Tool calls → solver/verify")
        Component(copilot, "ScheduleCopilotService", "Python + OpenAI API", "Chat copiloto")
        Component(pseudo, "ProfessorPseudonymService", "Python", "Tokeniza siglas p/ OpenAI")
    }

    Rel(copilot, pseudo, "anonymize / deanonymize")
    Rel(pseudo, rag, "corpus tokenizado")
    Rel(pseudo, bridge, "tokens → siglas reais antes exec")

    Rel(auth, rules, "coordenador_id")
    Rel(intake, catalog, "parse Mascara_Entrada_Provas.xlsx")
    Rel(intake, constraints, "export/import xlsx backup opcional")
    Rel(ingest, catalog, "import prova anterior")
    Rel(catalog, solver, "ExamCatalog normalizado")
    Rel(constraints, solver, "CalendarConstraints")
    Rel(constraints, verify, "mesma fonte feriados/bloqueios")
    Rel(ingest, solver, "grade horária")
    Rel(layout, solver, "template escrever()")
    Rel(ingest, docs, "blobs entrada")
    Rel(docs, rag, "chunk + index")
    Rel(solver, docs, "Proposta xlsx gerado")
    Rel(solver, rag, "reindex pós-geração")
    Rel(rules, solver, "perfil regras ativo")
    Rel(rules, copilot, "RuleSetSnapshot")
    Rel(solver, verify, "alocações")
    Rel(verify, calendar, "OK / PROBLEMA")
    Rel(verify, views, "PROBLEMA/AVISO")
    Rel(verify, copilot, "diagnóstico")
    Rel(rag, copilot, "rag_search")
    Rel(views, copilot, "estatísticas")
    Rel(copilot, bridge, "tool calling")
    Rel(bridge, solver, "run_partial_solver")
    Rel(bridge, verify, "get_verification_report")
    Rel(bridge, calendar, "apply_proposal")
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
| — | `IntakeTemplateService` — máscaras provas + bloqueios 🟡 |
| — | `CalendarBlockPicker` → `CalendarConstraintsService` 🟢 |
| `Klausurplan_2026_2SEM.xlsx` | `CalendarLayoutTemplate` — layout saída 🟢 |

## Frontend (alvo) 🟡 — componentes UI

| Componente UI | Feature Reversa |
|---|---|
| `RulesSelectionWizard` | Seleção regras Tela 1–2 |
| `IntakeTemplatePanel` | Download/upload máscara provas (opcional) 🟡 |
| `CalendarBlockPicker` | Malha calendário — clique dia/semana por turma/série 🟢 |
| `ExamCatalogEditor` | Grid aba `provas`: ordem · tempos · n_aulas_semanais 🟡 |
| `CalendarPreviewView` | Visualização read-only Proposta_3 por turma 🟢 |
| `CalendarEditor` | Refração manual (grid editável) |
| `ScheduleCopilotChat` | Chat copiloto pós-geração (Q&A + alterações) 🟡 |
| `ProblemViewsPanel` | Estatísticas / visões alinhadas ao copiloto 🟡 |
| `VerificationPanel` | Checklist PROBLEMA/AVISO |
| `CloseCalendarAction` | Fechar horário |
| `DonorEmailPanel` | Preview + envio e-mail doadores |
