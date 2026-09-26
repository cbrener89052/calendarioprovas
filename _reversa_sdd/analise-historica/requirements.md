# Requirements: Análise Histórica

> Identificador: `005-analise-historica`  
> Data: `2026-08-09`

## 1. Resumo executivo

Analisa calendários de semestres anteriores e compara percentuais de cessão entre semestres, servindo como benchmark para validar Proposta 3 e detectar drift de carga horária cedida.

## 2. Contexto

| Fonte | Trecho | Conf. |
|-------|--------|-------|
| `analisar_1semestre.py`, `comparar_semestres.py` | Scripts | 🟢 |
| `_reversa_sdd/domain.md` | Comparar percentual, não contagem absoluta | 🟢 |

## 3. Personas

| Persona | Objetivo | Cenário |
|---------|----------|---------|
| Coordenador | Benchmark antes/depois Proposta 3 | Compara 1sem vs 2sem |
| Gestão | Evidência de redução cessões | Relatório comparativo |

## 4. Regras

1. **RN-01:** Comparar **percentual** de cessão, não valores absolutos (semestres diferentes) 🟢
2. **RN-02:** Parser tolerante a variações texto células 🟢

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério | Conf. |
|----|-----------|------------|----------|-------|
| RF-01 | `tempos_do_texto(txt)` parse flexível | Must | Extrai lista tempos | 🟢 |
| RF-02 | Comparativo por turma/disciplina | Must | pct_1sem, pct_p3, variacao_pp | 🟢 |
| RF-03 | Relatório stdout/xlsx | Should | Tabela ordenada | 🟢 |
| RF-04 | Histórico no BD (plataforma v2) | Could | Query entre semestres | 🟡 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Comparativo semestres
  Dado xlsx 1sem2025 e calendário Proposta 3 2sem2026
  Quando comparar_semestres.py executa
  Então exibe variação em pontos percentuais por disciplina
```

## 8. MoSCoW

RF-01–RF-02 Must; RF-03 Should; RF-04 Could (v2 plataforma).

## 11. Histórico

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | Versão inicial | reversa-writer |
