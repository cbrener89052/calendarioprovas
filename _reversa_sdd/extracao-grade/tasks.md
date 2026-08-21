# Extração de Grade — Tarefas

## Pré-requisitos

- [ ] PDF golden 1º sem (`horarios_1semestre/`)
- [ ] `GRADE_TXT` 2º sem como referência paridade

## Tarefas

- [ ] T-01, Portar `extrair_grade_1semestre.extrair_turma` → `GradeUntisTextParser`
  - Origem: `extrair_grade_1semestre.py`
  - Confiança: 🟢

- [ ] T-02, API upload + blob storage
  - Confiança: 🟡

- [ ] T-03, Persistência `grade_horaria` (ERD)
  - Confiança: 🟡

- [ ] T-04, `GradePreviewView` integrado
  - Origem: ADR-013
  - Confiança: 🟡

- [ ] T-05, Validador turma × catálogo provas
  - Confiança: 🟡

- [ ] T-06, Parser 2º sem 2026 (eliminar GRADE_TXT hardcoded)
  - Confiança: 🔴

- [ ] T-07, Consolidar OCR 2025 (opcional)
  - Origem: `limpar_grade_2025.py`
  - Confiança: 🟡

## Ordem

T-01 → T-02 → T-03 → T-05 → T-04 → T-06
