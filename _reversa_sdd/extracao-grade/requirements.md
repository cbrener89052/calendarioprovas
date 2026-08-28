# Requirements: Extração de Grade Horária

> Identificador: `004-extracao-grade`
> Data: `2026-08-21`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

A feature **extracao-grade** converte PDFs Untis (horários de turma) em estruturas
`(turma, dia, tempo, disciplina, professor)` consumíveis pelo solver. No legado,
pipelines distintos para 2025 (OCR) e 1º sem 2026 (texto + hora de início). O
2º sem 2026 ativo usa **`GRADE_TXT` hardcoded** em `gerar_calendario.py` — não
passa pelos extractors.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confiança |
|-------|------------------|-----------|
| `_reversa_sdd/code-analysis.md#Módulo: extracao-grade` | 4 scripts + horarios2025 | 🟢 |
| `_reversa_sdd/flowcharts/extracao-grade.md` | Fluxos 2025 vs 2026 | 🟢 |
| `_reversa_sdd/data-dictionary.md#Grade horária` | Tupla canônica | 🟢 |
| `.reversa/context/user-requirements.md` | Grade obrigatória para fatoração | 🟢 |

## 3. Personas e cenários

| Persona | Objetivo | Cenário |
|---------|----------|---------|
| Coordenador (legado) | Atualizar grade após PDF Untis | Roda extractor + cola em `gerar_calendario.py` |
| Coordenador (plataforma) | Upload PDF/planilha | Blob → parser → preview → `grade_horaria` BD |
| Sistema | Validar antes do solver | Turma/disciplina/professor coerentes |

## 4. Regras de negócio

1. **RN-01:** Estrutura canônica `(turma, dia 1–5, tempo 1–11, disc, prof)`. 🟢
2. **RN-02:** Mapeamento hora→tempo no 1º sem (`TEMPOS` em `extrair_grade_1semestre.py`) confirmado pela escola. 🟢
3. **RN-03:** 2025 usa `CODE_MAP` + limpeza OCR (`limpar_grade_2025.py`). 🟢
4. **RN-04:** Grade do 2º sem 2026 **não** é extraída automaticamente hoje — `GRADE_TXT` manual. 🟢
5. **RN-05:** Plataforma Must aceitar upload PDF Untis (substitui hardcode). 🟢 ADR-015
6. **RN-06:** Parser dedicado 2º sem 2026 — Should no forward; legado mantém hardcode até lá. 🟡

## 5. Requisitos Funcionais — legado 🟢

| ID | Script | Entrada | Saída | Must |
|----|--------|---------|-------|------|
| RF-01 | `extrair_grade_2025.py` | PDF sem texto | `GRADE_BRUTA_2025` | Should |
| RF-02 | `limpar_grade_2025.py` | BRUTA + CODE_MAP | `GRADE_2025` | Should |
| RF-03 | `esqueleto_grade_2025.py` | Geometria PDF | auxiliar OCR | Could |
| RF-04 | `extrair_grade_1semestre.py` | PDF com texto | `grade_1semestre.py` | Should |
| RF-05 | Validar cabeçalho 5 dias (Mo–Fr) por página | PDF | erro se incompleto | Must |

## 6. Requisitos Funcionais — plataforma 🟡

| ID | Requisito | Prioridade | Critério de aceite |
|----|-----------|------------|--------------------|
| RF-06 | Upload PDF/planilha grade por calendário | Must | Blob + metadados semestre/turmas |
| RF-07 | `GradeParserService` — pipeline 1º sem (hora→tempo) | Must | Paridade `extrair_grade_1semestre` |
| RF-08 | Preview grade por turma antes de persistir | Must | Grid read-only (paridade ADR-013 aba grade) |
| RF-09 | Persistir `grade_horaria` PostgreSQL | Must | ERD `GRADE` / slots |
| RF-10 | Detectar turmas ausentes vs catálogo provas | Must | AVISO na ingestão |
| RF-11 | Pipeline OCR 2025 como fallback 🟡 | Could | Reuso `limpar_grade_2025` |

## 7. Critérios de Aceitação

```gherkin
Cenário: Extração 1º semestre por hora de início
  Dado PDF Untis com células disciplina + hora 8.05
  Quando extrair_grade_1semestre processa a turma 10C1
  Então slot (dia, tempo=2) recebe disciplina e professor corretos

Cenário: Upload grade na plataforma
  Dado coordenador envia PDF válido
  Quando parser conclui e coordenador confirma preview
  Então grade_horaria persiste e CalendarSolver pode carregar slots
```

## 8. Lacunas

- 🟡 Parser PDF 2º sem 2026 — T-parser-2sem no forward (legado: `GRADE_TXT` temporário)
- 🟡 Unificar extractors 2025/2026 num serviço
- 🟡 Siglas professor: normalização `/` e `-` na ingestão

## 9. Histórico

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-21 | Versão inicial | reversa-writer |
