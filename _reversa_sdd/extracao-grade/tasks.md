# Extração de Grade — Tarefas

> Contrato compartilhado: `GradeSnapshot` em `packages/ingest/ingest/models.py` (ADR-008). Solver consome snapshot **aprovado**, nunca re-parse PDF.

- [ ] T-01 — Mapeamento geométrico `celula_da`
  - Origem: `extrair_grade_2025.py`
  - Confiança: 🟢

- [ ] T-02 — Pipeline texto nativo PDF
  - Confiança: 🟢

- [ ] T-03 — Fallback OCR tesseract
  - Confiança: 🟢

- [x] T-04 — Export grade → tabela `grade_celula` (ERD)
  - Entrega: migration T3b + `GradeSnapshot` → INSERT via API/worker
  - Confiança: 🟢

- [ ] T-05 — Job assíncrono upload plataforma
  - Depende: Tarefa 4 reconstruction-plan (API upload)
  - Confiança: 🟡

- [x] T-06 — CLI check-in revisor (`python -m ingest.checkin`)
  - Entrega: T3d — bloqueia `--approve` com avisos críticos
  - Confiança: 🟢

## Testes

- [ ] TT-01 — PDF referência 2025 vs grade manual
- [ ] TT-02 — Avisos em célula ilegível
- [ ] TT-03 — Check-in legacy `.py` → checksum estável

## Ordem

T-01 → T-02 → T-03 → T-04 ✅ → T-05  
T-06 ✅ (paralelo, não bloqueia extração PDF)
