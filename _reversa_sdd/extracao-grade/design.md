# Extração de Grade — Design Técnico

> Feature: `extracao-grade` | Legado: `extrair_grade_*.py`

## Interface legado

| Script | Entrada | Saída | Tecnologia |
|--------|---------|-------|------------|
| `extrair_grade_2025.py` | PDF raster | dict bruto | pymupdf + Tesseract 🟡 |
| `limpar_grade_2025.py` | GRADE_BRUTA | GRADE_2025 | CODE_MAP 🟢 |
| `extrair_grade_1semestre.py` | PDF texto | `grade_1semestre.py` | pymupdf + TEMPOS 🟢 |

Tupla canônica: `(turma, dia, tempo, disc, prof)` — ver `data-dictionary.md`.

## Fluxo 1º semestre (referência implementada) 🟢

1. Abrir PDF — uma página por turma (`9C1`…`12C2`)
2. Detectar colunas Mo–Fr (`limites_das_colunas`)
3. Agrupar palavras por linha — hora de início → `TEMPOS`
4. Extrair disciplina, professor (`*`), sala
5. Gravar módulo Python importável

## Fluxo 2º sem 2026 (as-is) 🟢

`GRADE_TXT` multiline string em `gerar_calendario.py` → parse → `GRADES` dict.

## Plataforma alvo 🟡

| Componente | Papel |
|------------|-------|
| `GradeParserService` | Orquestra parsers por formato/semestre |
| `GradeUntisTextParser` | Port de `extrair_grade_1semestre` |
| `GradeOcrParser` | Port 2025 (opcional) |
| `GradePreviewView` | UI read-only pós-upload (ADR-013) |

### API

| Método | Caminho | Descrição |
|--------|---------|-----------|
| POST | `/api/v1/calendars/{id}/grade/upload` | PDF/xlsx |
| GET | `/api/v1/calendars/{id}/grade/preview` | Grid por turma |
| POST | `/api/v1/calendars/{id}/grade/confirm` | Persiste |

## Dependências

- pymupdf 🟢
- Tesseract (2025) 🟡
- `geracao-calendario` consome grade 🟢
- `ExamCatalog` validação cruzada 🟡

## Riscos

- 🔴 PDF Untis muda layout entre semestres
- 🟡 Duplicação GRADE_TXT vs BD na migração
