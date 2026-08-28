# Spec Impact Matrix — calendarioprovas

> Gerado pelo Arquiteto (Reversa) em 2026-08-15  
> Mapeia componentes legado → features → requisitos → artefatos alvo

---

## Legenda

- **Impacto:** H (alto) | M (médio) | L (baixo) | — (n/a)
- **Confiança:** 🟢 confirmado | 🟡 inferido

---

## Matriz — componentes legado × features

| Componente legado | geracao-calendario | verificacao | exportacao-relatorios | regras-negocio | plataforma-multi-coord |
|---|---|---|---|---|---|
| `gerar_calendario.py` | **H** 🟢 | M 🟢 | M 🟢 | M 🟢 | **H** 🟡 |
| `verificar_calendario.py` | M 🟢 | **H** 🟢 | L 🟢 | M 🟢 | **H** 🟡 |
| `exportar_relatorio_trocas.py` | — | L 🟢 | **H** 🟢 | L 🟢 | **H** 🟡 (e-mail) |
| `exportar_tempos_cedidos.py` | — | M 🟢 | **H** 🟢 | M 🟢 | M 🟡 |
| `exportar_tabelas_turma.py` | — | L 🟢 | **H** 🟢 | — | M 🟡 |
| `exportar_provas_por_professor.py` | — | L 🟢 | **H** 🟢 | — | M 🟡 |
| `calendario-provas/SKILL.md` | **H** 🟢 | **H** 🟢 | L 🟢 | **H** 🟢 | **H** 🟡 |
| `extrair_grade_*.py` | L 🟢 | — | — | — | M 🟡 |
| Git main/producao | L 🟢 | L 🟢 | L 🟢 | — | M 🟡 |

---

## Matriz — requisitos usuário × componentes alvo

| Requisito (user-requirements) | Componentes impactados | Impacto | Status |
|---|---|---|---|
| Multi-coordenador + PostgreSQL | API, DB, Auth, Blob | **H** | 🔴 não implementado |
| Seleção regras Tela 1–2 | RulesCatalogService, Frontend, DB | **H** | 🔴 |
| Fatoração automática | CalendarSolver | **H** | 🟢 legado CLI |
| Refração manual | CalendarEditor, Blob | **H** | 🟢 legado xlsx |
| Copiloto OpenAI + RAG | ScheduleCopilotService, RagIndexService, PythonActionBridge, Chat UI | **H** | 🔴 ADR-008 |
| Catálogo provas flexível | ExamCatalogService, ExamCatalogEditor | **H** | 🔴 ADR-010 |
| Fechar horário | CalendarLifecycle | M | 🟡 Git hoje |
| E-mail doadores (manual) | DonorEmailService, SMTP, ENVIO_EMAIL | **H** | 🔴 |
| Deploy híbrido Docker | Infra, Blob, SMTP config | M | 🔴 |
| Sync skill GitHub | sources.json, RegraCatalogo seed | M | 🟡 parcial |

---

## Matriz — regra de domínio × implementação

| Regra (domain.md) | gerar_calendario | verificar | skill | Gap |
|---|---|---|---|---|
| R-P1 Professor presente | 🟢 | 🟢 item 0 | 🟢 | — |
| C1–C5 Cessão P3 | 🟢 Cessoes | 🟢 10b | 🟢 | — |
| R-FIL-SOC | 🟡 implícito | 🟢 COORDENACAO_EXCECAO | 🟢 | só verificador |
| ENEM semanas | 🔴 legado | 🟡 forward | 🟢 doc | **Must plataforma** ADR-015 |
| Véspera 2CH 9C | 🔴 | 🔴 | 🟢 doc | **Won't v1** manual |
| R-2CH período | 🔴 | 🔴 | 🟢 doc | **Won't v1** manual |
| E-mail doadores | 🔴 | — | — | **plataforma** |

---

## Matriz — migração legado → plataforma

| Artefato legado | Serviço alvo | Estratégia | Risco |
|---|---|---|---|
| `gerar_calendario.py` | `CalendarSolver` module | Extrair funções; manter testes caracterização | H |
| Constantes GRADES | `IngestService` + DB grade | Import xlsx/PDF; depreciar hardcode | M |
| Scripts export | `ReportExporter` | Reusar parsers; API gera blob | L |
| Pastas locais | Blob storage | Upload; metadados PG | M |
| `.bat` Git sync | CI/CD + lifecycle API | Fase 2; manter Git paralelo | L |
| Skill | `regra_catalogo` seed | Sync sources.json | M |

---

## Componentes com maior fan-out (prioridade Writer/Migrate)

1. **`gerar_calendario.py`** — 5 features + plataforma
2. **`calendario-provas/SKILL.md`** — regras + verificação + UI catálogo
3. **`exportar_relatorio_trocas.py`** — relatório + e-mail doadores
4. **`verificar_calendario.py`** — gate qualidade pré-fechamento

---

## Rastreabilidade para specs SDD (Writer)

| Feature folder (granularity=feature) | Specs a gerar |
|---|---|
| `geracao-calendario` | requirements, design, tasks |
| `verificacao-calendario` | requirements, design, tasks |
| `exportacao-relatorios` | requirements, design, tasks |
| `regras-negocio` | requirements (catálogo), design |
| `plataforma-multi-coordenador` | requirements (auth, e-mail, regras UI), design, ERD ref |

Referência organização: `.reversa/config.toml` → `[specs].granularity = feature`
