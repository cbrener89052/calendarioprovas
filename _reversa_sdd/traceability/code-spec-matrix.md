# Code ↔ Spec Matrix

> Gerado pelo Redator (Reversa Fase 4), doc_level=completo.  
> Mapeia arquivos do legado às pastas de feature em `_reversa_sdd/<feature>/`.

---

## Matriz principal

| Arquivo do legado | Unit / Feature | Cobertura | Arquivos spec |
|---|---|---|---|
| `gerar_calendario.py` | `geracao-calendario/` | 🟢 | requirements, design, tasks |
| `verificar_calendario.py` | `verificacao-calendario/` | 🟢 | requirements, design, tasks |
| `exportar_tabelas_turma.py` | `exportacao-relatorios/` | 🟢 | requirements, design, tasks |
| `exportar_tempos_cedidos.py` | `exportacao-relatorios/` | 🟢 | requirements, design, tasks |
| `extrair_grade_2025.py` | `extracao-grade/` | 🟢 | requirements, design, tasks |
| `extrair_grade_1semestre.py` | `extracao-grade/` | 🟢 | requirements, design, tasks |
| `esqueleto_grade_2025.py` | `extracao-grade/` | 🟡 | design (template) |
| `limpar_grade_2025.py` | `extracao-grade/` | 🟡 | — (utilitário limpeza OCR) |
| `contar_2sem_2025.py` | `analise-historica/` | 🟡 | — (contagem auxiliar) |
| `horarios2025/*.py` | `extracao-grade/` | 🟡 | artefatos gerados, não fonte |
| `analisar_1semestre.py` | `analise-historica/` | 🟢 | requirements, design, tasks |
| `analisar_2sem_2025.py` | `analise-historica/` | 🟢 | requirements, design, tasks |
| `comparar_semestres.py` | `analise-historica/` | 🟢 | requirements, design, tasks |
| `exportar_regras_pdf.py` | `regras-negocio/` | 🟢 | requirements, design, tasks |
| `.claude/skills/calendario-provas/SKILL.md` | `regras-negocio/` | 🟢 | requirements, design, tasks |
| `.reversa/context/user-requirements.md` | `plataforma-multi-coordenador/` | 🟢 | requirements, design, tasks, contracts |
| `.reversa/context/sync-regras.md` | `regras-negocio/` | 🟢 | design |
| `.reversa/context/sources.json` | `regras-negocio/` | 🟢 | design |

---

## Arquivos sem unit dedicada (n/a ou parcial)

| Arquivo | Cobertura | Nota |
|---|---|---|
| `*.bat` (git sync Windows) | n/a | Substituído por CI/CD na plataforma |
| `referencia/*.md` | 🟡 | Citado em domain.md / addenda |
| `CLAUDE.md`, `.cursorrules` | n/a | Meta-config projeto |
| `.reversa/*` | n/a | Framework Reversa |
| `_reversa_sdd/*.md` (raiz) | n/a | Artefatos fases 1–3 (input Redator) |

---

## Cobertura por feature

| Feature | Arquivos legado mapeados | % estimado |
|---|---|---|
| geracao-calendario | 1 principal | 🟢 100% |
| verificacao-calendario | 1 | 🟢 100% |
| exportacao-relatorios | 2 | 🟢 100% |
| extracao-grade | 3 | 🟢 ~95% |
| analise-historica | 3 | 🟢 100% |
| regras-negocio | 2 + skill | 🟢 100% |
| plataforma-multi-coordenador | — (greenfield) | 🟡 specs only |

**Cobertura global legado:** ~95% dos scripts Python mapeados a uma feature.

---

## Lacunas código → spec

| Lacuna | Feature | Status |
|---|---|---|
| LP/LIT/RED 10 dias | 🟢 PR #18 | geracao + verificacao + regras |
| Validação cores ARGB | verificacao-calendario | 🔴 |
| RuleContext / toggles | regras + plataforma | 🟡 spec, sem código |
| API FastAPI | plataforma | 🟡 OpenAPI draft |

---

## Rastreabilidade inversa (spec → código)

| Spec | Implementação alvo |
|---|---|
| `geracao-calendario/tasks.md` T-06 | `gerar_calendario.py` |
| `verificacao-calendario/tasks.md` T-04 | `verificar_calendario.py` |
| `plataforma-multi-coordenador/tasks.md` T-08 | worker + refactor gerador |
| `regras-negocio/tasks.md` T-09 | ✅ PR #18 |

---

## Histórico

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-10 | Sync PR #18 | reversa-sync |
| 2026-08-09 | Matriz inicial Fase 4 | reversa-writer |
