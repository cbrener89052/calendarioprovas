# Extração de Grade — Design Técnico

## Interface

| Símbolo | Assinatura | Retorno |
|---------|-----------|---------|
| `celula_da` | `(x, y)` | `(dia, tempo) \| None` |
| `extrair_turma` | `(ws)` | `(grade, avisos)` |

## Fluxo Principal

1. Abrir PDF (pymupdf) 🟢
2. Detectar texto vs imagem 🟢
3. Mapear retângulos → células (dia, tempo) 🟢
4. Extrair disciplina/professor por célula 🟢
5. Acumular avisos (vazio, OCR baixa confiança) 🟢
6. Serializar grade (`.py` legado ou INSERT BD) 🟢

## Dependências

- pymupdf (fitz) 🟢
- tesseract (OCR) 🟢
- esqueleto_grade_2025.py (template) 🟢

## API futura 🟡

| Método | Caminho |
|--------|---------|
| POST | `/api/v1/grades/upload` |
| GET | `/api/v1/grades/jobs/{id}` |

## Riscos

- 🔴 OCR errors propagam para calendário errado — exige revisão
- 🟡 Layout Untis muda entre anos — parametrizar coordenadas
