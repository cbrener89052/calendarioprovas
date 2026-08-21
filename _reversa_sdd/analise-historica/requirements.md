# Requirements: Análise Histórica

> Identificador: `005-analise-historica`
> Data: `2026-08-21`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo executivo

Feature **analise-historica** compara calendários e cessões entre semestres —
benchmark de tempos cedidos, reconstrução de uso em 2025 e validação de
propostas passadas. Scripts ad hoc; na plataforma vira dashboards e corpus
RAG para o copiloto.

## 2. Contexto legado

| Fonte | Confiança |
|-------|-----------|
| `_reversa_sdd/code-analysis.md#Módulo: analise-historica` | 🟢 |
| `analisar_1semestre.py`, `analisar_2sem_2025.py`, `contar_2sem_2025.py`, `comparar_semestres.py` | 🟢 |

## 3. Regras de negócio

1. **RN-01:** Análises leem **xlsx/planilhas históricas**, não memória do solver. 🟢
2. **RN-02:** `contar_2sem_2025` infere duração só por `(N)` no texto da célula. 🟢
3. **RN-03:** `comparar_semestres` cruza % cessão 1º sem ocorrido vs Proposta 3. 🟢
4. **RN-04:** Resultados são **consultivos** — não alteram calendário corrente. 🟢

## 4. Requisitos Funcionais — legado

| ID | Script | Saída | Must |
|----|--------|-------|------|
| RF-01 | `analisar_1semestre.py` | Cessões reais vs `GRADE_1SEM` | Should |
| RF-02 | `analisar_2sem_2025.py` | Métricas 2º sem 2025 | Should |
| RF-03 | `contar_2sem_2025.py` | Tempos usados reconstruídos | Should |
| RF-04 | `comparar_semestres.py` | Comparativo % cessões | Should |

## 5. Requisitos Funcionais — plataforma 🟡

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-05 | Armazenar snapshots históricos por semestre | Should |
| RF-06 | Dashboard cessões: semestre atual vs anterior | Should |
| RF-07 | Copiloto consulta estatísticas via `CalendarViewsService` | Must |
| RF-08 | Importar xlsx semestre anterior como referência catálogo 🟡 | Could |

## 6. Critérios de Aceitação

```gherkin
Cenário: Comparativo de cessões
  Dado Proposta_3 fechada do semestre anterior persistida
  Quando coordenador abre dashboard histórico
  Então vê percentual de cessões vs semestre corrente
```

## 7. Lacunas

- 🔴 Sem BD histórico — só arquivos locais
- 🟡 Integração formal com `CalendarViewsService`

## 8. Histórico

| Data | Alteração |
|------|-----------|
| 2026-08-21 | Versão inicial |
