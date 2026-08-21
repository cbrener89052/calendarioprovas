# Code ↔ Spec Matrix

> Gerado pelo Redator (Reversa) | 2026-08-21

| Arquivo legado | Unit / spec | Cobertura |
|----------------|-------------|-----------|
| `gerar_calendario.py` | `geracao-calendario/` | 🟢 |
| `verificar_calendario.py` | `verificacao-calendario/` | 🟢 |
| `exportar_tabelas_turma.py` | `exportacao-relatorios/` | 🟢 |
| `exportar_tempos_cedidos.py` | `exportacao-relatorios/` | 🟢 |
| `exportar_relatorio_trocas.py` | `exportacao-relatorios/` | 🟢 |
| `exportar_provas_por_professor.py` | `exportacao-relatorios/` | 🟢 |
| `exportar_regras_pdf.py` | `exportacao-relatorios/` | 🟡 |
| `extrair_grade_2025.py` | `extracao-grade/` | 🟢 |
| `extrair_grade_1semestre.py` | `extracao-grade/` | 🟢 |
| `limpar_grade_2025.py` | `extracao-grade/` | 🟢 |
| `esqueleto_grade_2025.py` | `extracao-grade/` | 🟡 |
| `analisar_1semestre.py` | `analise-historica/` | 🟢 |
| `analisar_2sem_2025.py` | `analise-historica/` | 🟢 |
| `contar_2sem_2025.py` | `analise-historica/` | 🟢 |
| `comparar_semestres.py` | `analise-historica/` | 🟢 |
| `.claude/skills/calendario-provas/SKILL.md` | `regras-negocio/` | 🟢 |
| `.reversa/context/user-requirements.md` | `plataforma-multi-coordenador/` | 🟢 |
| `commit_github.bat` | `plataforma-multi-coordenador/` | 🟡 |
| `horarios2025/*.py` | `extracao-grade/` | 🟡 |
| `Klausurplan_2026_2SEM.xlsx` | `geracao-calendario/` ADR-010 | 🟢 |
| `_reversa_sdd/templates/*.md` | `geracao-calendario/` | 🟢 |
| `_reversa_sdd/ui/*.md` | `plataforma-multi-coordenador/` | 🟢 |

**Cobertura estimada:** 16/16 scripts Python mapeados; plataforma alvo consolidada em `plataforma-multi-coordenador/`.

**Arquivos sem unit dedicada:** `commit_github.bat` (fluxo git documentado em ADR-004).
