# Requirements: Extração de Grade

> Identificador: `004-extracao-grade`  
> Data: `2026-08-09`

## 1. Resumo executivo

Extrai grade horária semanal de PDFs Untis (texto nativo ou OCR) para estrutura Python `(turma, dia, tempo) → disciplina`, alimentando o gerador de calendário. Suporta mapeamento geométrico de células e conversão hora→tempo.

## 2. Contexto

| Fonte | Trecho | Conf. |
|-------|--------|-------|
| `_reversa_sdd/flowcharts/extracao-grade.md` | Pipeline PDF → grade | 🟢 |
| `extrair_grade_2025.py`, `extrair_grade_1semestre.py` | Scripts | 🟢 |
| `_reversa_sdd/architecture.md` | pymupdf + tesseract | 🟢 |

## 3. Personas

| Persona | Objetivo | Cenário |
|---------|----------|---------|
| Coordenador | Atualizar grade a cada semestre | Roda extrator após export Untis |
| Plataforma | Upload PDF assíncrono | Job OCR → grade no BD |

## 4. Regras de negócio

1. **RN-01:** Mapeamento dia/tempo 1–11 conforme horários escola (7h15–15h55) 🟢
2. **RN-02:** OCR quando PDF sem texto selecionável 🟢
3. **RN-03:** Avisos para células ambíguas/não mapeadas 🟢

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério | Conf. |
|----|-----------|------------|----------|-------|
| RF-01 | `celula_da(x,y)` → (dia, tempo) | Must | Coordenadas PDF → grade | 🟢 |
| RF-02 | `extrair_turma(ws)` → (grade, avisos) | Must | Dict completo por turma | 🟢 |
| RF-03 | Suporte PDF texto + OCR | Must | Fallback tesseract | 🟢 |
| RF-04 | Gerar `.py` ou persistir BD | Should | Compatível com gerador | 🟢 |
| RF-05 | Upload + job assíncrono (plataforma) | Should | Status + preview avisos | 🟡 |

## 6. RNFs

| Tipo | Requisito | Evidência | Conf. |
|------|-----------|-----------|-------|
| Dependência | pymupdf, tesseract opcional | scripts | 🟢 |
| Qualidade | Avisos human-review para OCR ruim | avisos list | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: PDF Untis com texto
  Dado PDF 2sem2026 exportado do Untis
  Quando extrair_grade executa
  Então grade 9C1 contém disciplinas por (dia,tempo) sem avisos críticos

Cenário: OCR necessário
  Dado PDF apenas imagem
  Quando pipeline usa tesseract
  Então grade parcial + lista avisos para revisão manual
```

## 8. MoSCoW

RF-01–RF-03 Must; RF-04 Should; RF-05 Should (plataforma).

## 10. Lacunas

- 🟡 UI revisão humana de avisos OCR na plataforma
- 🟡 Validação automática grade vs modelo calendário

## 11. Histórico

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | Versão inicial | reversa-writer |
